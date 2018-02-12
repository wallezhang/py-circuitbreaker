# -*- coding: utf-8 -*-

import threading
import time

import bucket

OPEN = 0
CLOSE = 1
HALF_OPEN = 2


class SlidingWindow(object):
    def __init__(self, rate, period, half_seconds, sample_count, step, threshold_percentage):
        """
        滑动窗口实现类
        """
        self.rate = rate
        self.period = period
        self.half_seconds = half_seconds
        self.sample_count = sample_count
        self.tail = 0
        self.buckets = []
        self.step = step
        self.status = CLOSE
        self._semaphore = threading.Semaphore(1)
        self._threshold_percentage = threshold_percentage

        for _ in xrange(period / rate):
            self.buckets.append(bucket.Bucket())

    def increase_total(self):
        self.buckets[self.tail].add_total(self.step)

    def increase_fail(self):
        self.buckets[self.tail].add_fail(self.step)

    def _calculate_failure_rate(self):
        """
        计算失败率
        :return:
        """
        total, fail = 0, 0
        for i in xrange(self.tail + 1):
            total += self.buckets[i].total
            fail += self.buckets[i].fail
        return float(fail) / float(total)

    def _total(self):
        total = 0
        for i in xrange(self.tail + 1):
            total += self.buckets[i].total
        return total

    def acquire_sem(self):
        return self._semaphore.acquire(False)

    def release_sem(self):
        return self._semaphore.release()

    def start(self):
        thread = threading.Thread(target=self.increase_tail, name='increase_tail_thread')
        thread.setDaemon(True)
        thread.start()

    def increase_tail(self):
        while 1:
            # 判断是否需要打开熔断器
            if self.status == CLOSE and self._total() > self.sample_count and self._calculate_failure_rate() > self._threshold_percentage:
                self.set_open()
            if self.tail + 1 >= self.period / self.rate:
                tmp_buckets = self.buckets[1:self.tail + 1]
                tmp_buckets.append(bucket.Bucket())
                self.buckets = tmp_buckets
            else:
                self.tail += 1

            time.sleep(self.rate / 1000)

    def _set_half_open(self):
        self.status = HALF_OPEN

    def set_open(self):
        self.status = OPEN
        threading.Timer(self.half_seconds / 1000, self._set_half_open).start()
