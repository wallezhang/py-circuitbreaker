# -*- coding: utf-8 -*-

import threading

from circuitbreaker.bucket import Bucket

COUNT = 100000


def runner(bucket):
    for _ in xrange(COUNT):
        bucket.add_fail(1)


def test_single_thread():
    """
    测试单线程下增加数量是否正确
    :return:
    """
    b = Bucket()
    for _ in xrange(COUNT):
        b.add_fail(1)

    for _ in xrange(COUNT):
        b.add_total(1)

    assert b.total == COUNT * 2
    assert b.fail == COUNT


def test_multi_thread():
    """
    测试多线程下数量是否正确，线程安全
    :return:
    """
    threads = []
    b = Bucket()
    for i in xrange(10):
        threads.append(threading.Thread(target=runner, args=(b,), name='worker%s' % i))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    assert b.total == 10 * COUNT
    assert b.fail == 10 * COUNT
