# -*- coding: utf-8 -*-
import threading


class Bucket(object):
    """
    滑动窗口中的桶对象，桶中包含两个计数器变量，失败和总量
    """

    def __init__(self):
        self.total = 0
        self.fail = 0
        self.lock = threading.Lock()

    def add_fail(self, step):
        """
        失败数增加步长个单位，线程安全
        :param step: 步长。默认为1
        :return:
        """
        with self.lock:
            self.total += step
            self.fail += step

    def add_total(self, step):
        """
        总数增加步长个单位，线程安全
        :param step: 步长，默认为1
        :return:
        """
        with self.lock:
            self.total += step
