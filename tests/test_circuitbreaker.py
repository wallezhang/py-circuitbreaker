# -*- coding: utf-8 -*-

import threading
import time

from circuitbreaker.circuitbreaker import initialize_circuit_breaker, circuit_breaker
from circuitbreaker.slidingwindow import OPEN, HALF_OPEN, CLOSE

RATE = 1000
PERIOD = 10 * 1000
VOLUME_THRESHOLD = 10
SLEEP_WINDOW_IN_MILLISECONDS = 2000

window = initialize_circuit_breaker(RATE, PERIOD, VOLUME_THRESHOLD, SLEEP_WINDOW_IN_MILLISECONDS)


def judge_fail_fn(res):
    return res is None


def fallback_fn(*args, **kwargs):
    return 'fallback'


@circuit_breaker(window, judge_fail_fn, fallback_fn)
def handler(*args):
    return args[0]


def test_bucket_len():
    assert len(window.buckets) == PERIOD / RATE


def test_get_sem_half_open():
    assert window.acquire_sem() is True
    assert window.acquire_sem() is False
    window.release_sem()


def test_circuit():
    threads = []
    for _ in xrange(25):
        threads.append(threading.Thread(target=handler, args=(None,)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    time.sleep(1.5)

    assert window.status == OPEN
    assert handler(1) == 'fallback'

    time.sleep(SLEEP_WINDOW_IN_MILLISECONDS / 1000)

    assert window.status == HALF_OPEN
    handler(1)
    assert window.status == CLOSE
