# -*- coding: utf-8 -*-
import threading


class Bucket(object):
    """
    The bucket of sliding window includes two counters, total and fail
    """

    def __init__(self):
        self.total = 0
        self.fail = 0
        self.lock = threading.Lock()

    def add_fail(self, step):
        """
        Add fail counter by step. Thread safe.
        :param step: default is 1
        :return:
        """
        with self.lock:
            self.total += step
            self.fail += step

    def add_total(self, step):
        """
        Add total counter by step. Thread safe.
        :param step: default is 1
        :return:
        """
        with self.lock:
            self.total += step
