from __future__ import annotations

from collections import OrderedDict
from itertools import cycle
import logging
from multiprocessing import Process, Queue
import queue
import random
from threading import Thread
import time
from typing import Callable, Dict, Iterable, List, Optional, Tuple, Union


logger = logging.getLogger(__name__)


class PrefetchGeneratorUnit(Process):
    def __init__(self, iterable: Iterable, num_prefetch: int, gid: int, processing_func: Optional[Callable] = None):
        """Prefetch Generator
        
        Args:
            iterable (Iterable): 데이터
            # queue (Queue): 데이터 반환할 큐
            num_prefetch (int): prefetch 개수
            gid (int): generator id
            processing_func (Callable): (Optional) 데이터 처리 함수
        """
        Process.__init__(self)
        self.iterable = iterable
        self.queue = Queue(maxsize=num_prefetch)
        self.num_prefetch = num_prefetch
        self.gid = gid
        self.processing_func = processing_func
        self.daemon = True
        self.start()

    def run(self):
        try:
            for idx, item in enumerate(self.iterable):
                # processing_func가 있으면 processing_func(item) 반환
                # # 없으면 그냥 item 반환
                item = item if self.processing_func is None else self.processing_func(item)
                # queue에 num_prefetch만큼 데이터가 있으면 여기서 멈춰있음
                # put에 넣는 첫번째 인자는 데이터, 두번째 인자는 실패 여부
                # logger.info(F"empty: {self.queue.empty()}, full: {self.queue.full()}, size: {self.queue.qsize()}")
                self.queue.put((item, self.gid, idx, False))
        except Exception as e:
            self.queue.put((e, self.gid, idx, True))
        finally:
            self.queue.put((StopIteration, self.gid, idx, True))


class PrefetchGenerator(Thread):
    """데이터를 병렬로 처리하는 generator

    Args:
        iterator (Union[List, Tuple, Dict, str]): iterable 데이터. generator는 지원하지 않음
        num_prefetch (int): prefetch 개수
        num_workers (int): 최대 Process 수. num_prefetch보다 작은 경우 num_prefetch와 같은 값으로 변경됨
        ordered (bool): 데이터 순서를 유지할 것인지(기본값=True)
        shuffle (bool): 데이터를 섞을 것인지(기본값=False). ordered = True 인 경우, shuffle은 항상 False
        processing_func (Callable): (Optional) 데이터 처리 함수
    """
    def __init__(self, iterator: Union[Dict, List, Tuple], num_prefetch: int = 1, num_workers: int = 1, ordered: bool = True, shuffle: bool = False, processing_func: Optional[Callable] = None) -> None:
        Thread.__init__(self)
        self._reset_states()
        self.iterator = iterator
        self.shuffle = shuffle
        if self.shuffle:
            self.ordered = False 
        else:
            self.ordered = ordered
        self.num_workers = min(num_prefetch, num_workers)
        self.num_prefetch = num_prefetch
        self.processing_func = processing_func
        self._continue = True
        self._is_running = True
        self._units = self.make_units()
        self.daemon = True
        self.start()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def _reset_states(self):
        """iteration 상태를 초기화"""
        # self.results에 전처리가 끝난 데이터를 {index: item} 형태로 저장
        # ordered=True 이면 self._next_idx를 0부터 차례로 증가시키며 데이터를 꺼냄
        # ordered=False 이면 self._next_idx는 사용되지 않으며, 데이터 처리가 끝난 순서대로 데이터를 꺼냄

        # self._pendding=True이면 PrefetchGeneratorUnit에서 데이터를 꺼내야하는 상태를 의미함

        # self._stoped_units는 데이터 처리가 끝난 PrefetchGeneratorUnit의 개수를 의미하며,
        # self._stoped_units와 self.num_workers가 같아지면 모든 unit의 작업이 끝난 것을 의미함
        self.results = OrderedDict()
        self._next_idx = 0
        self._pendding = False
        self._stoped_units = 0

    def make_units(self) -> Dict[int, PrefetchGeneratorUnit]:
        """self.num_workers만큼 PrefetchGeneratorUnit 생성
        
        여러 유닛에 데이터를 순차적으로 할당
        iterator = [1, 2, 3, 4], num_workers = 2 인 경우,
        unit1에는 [1, 3], unit2에는 [2, 4]가 할당됨

        Returns:
            (Dict[int, PrefetchGeneratorUnit]): gid(PrefetchGeneratorUnit의 번호)를 key로 가지는 dictionary
        """
        iterator = self.iterator[:]
        if self.shuffle:
            random.shuffle(iterator)
        num_prefetch_each_workers = max(self.num_prefetch//self.num_workers + (1 if self.num_prefetch%self.num_workers != 0 else 0) -1, 1)
        units = {gid: PrefetchGeneratorUnit(iterator[gid::self.num_workers], num_prefetch_each_workers, gid, self.processing_func) for gid in range(self.num_workers)}
        return units

    def run(self):
        """여러 PrefetchGeneratorUnit에서 데이터를 꺼냄
        
        유닛에서 데이터를 꺼내서 self.results에 저장
        """
        def _run():
            # 한 번의 iteration을 처리하는 함수
            # 새로운 iteration을 의미하므로 self._reset_states()를 호출해서 상태 초기화

            # unit의 작업이 끝났다고해서 iteration이 종료되는 것은 아니며,
            # self.results에 저장해놓은 데이터까지 소진해야 완전히 종료됨

            # unit의 작업이 끝나고, self.results가 빈 경우 self._continue = False로 만듦
            # self._continue는 iteration을 종료하는 조건으로 사용됨

            self._reset_states()
            _c = cycle(range(self.num_workers))  # 데이터를 꺼낼 PrefetchGeneratorUnit의 index를 순차적으로 출력
            while self._stoped_units < self.num_workers and self._is_running:
                try:
                    if self._pendding:
                        # item: 데이터
                        # gid: unit의 번호
                        # idx: unit 내부의 몇 번째 데이터인지
                        # err: 오류 여부. 오류가 아니면 False
                        item, gid, idx, err = self._units[next(_c)].queue.get_nowait()

                        # 전체 데이터에서의 index 계산
                        total_idx = gid+idx*self.num_workers
                        if not err:
                            self.results[total_idx] = item
                        else:
                            if item is StopIteration:
                                # unit 하나가 종료됨
                                self._stoped_units += 1
                                self._units[gid].terminate()
                            else:
                                logger.debug(f"StopIteration말고 다른 오류 발생 {e}", exc_info=True)
                                self._continue = False
                                raise item
                    else:
                        # self._pendding=True가 될때까지, 즉 __next__가 수행될때까지 대기
                        # unit에서 데이터 처리는 정상적으로 수행되고 있음
                        time.sleep(0.01)
                except queue.Empty:
                    # unit에서 꺼낼 데이터가 없음
                    # 잠깐 대기
                    time.sleep(0.01)
                except Exception as e:
                    logger.debug(f"여기에 무슨 오류가 오는지 모름 {e}", exc_info=True)
                    pass
            self._continue = False

        while self._is_running:
            _run()

    def stop(self):
        """PrefetchGenerator thread 종료"""
        self._is_running = False

    def __next__(self):
        while True:
            if not self._is_running:
                # run이 완료되지 않은 상태에서 self.stop()이 호출된 경우
                # 작업중인 unit을 모두 종료하고 StopIteration을 일으킨다.
                [_unit.terminate() for _unit in self._units.values()]
                raise StopIteration
            if not self._continue:
                # iteration이 정상적으로 한 번 끝난 경우
                # results에서 꺼낼 데이터도 없고, unit도 모두 종료된 상태
                raise StopIteration
            if (self._next_idx in self.results if self.ordered else self.results):
                # self.ordered=True 이면, self.results에서 next_idx를 꺼내고
                # self.ordered=False 이면, popitem(False)로 가장 오래된 데이터부터 꺼냄
                item = self.results.pop(self._next_idx) if self.ordered else self.results.popitem(False)[1]
                self._pendding = False
                self._next_idx +=1
                return item
            else:
                # unit에서 데이터가 준비될때까지 대기하기 위해서 진입하는 조건문
                # sleep이 없는 경우 불필요하게 자원을 많이 사용할 수 있어서 제약을 둠
                self._pendding = True
                time.sleep(0.01) 
          
    def __iter__(self):
        # self._continue=False인 경우는, iter가 한 번 실행된 이후를 의미함
        # unit을 다시 만듦
        if self._is_running:
            if not self._continue:
                self._continue = True
                self._units = self.make_units() 
            return self
        else:
            raise ValueError("This is a terminated thread.")
