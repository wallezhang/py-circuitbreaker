# -*- coding: utf-8 -*-

import logging
from functools import wraps

import slidingwindow


def circuit_breaker(window, judge_fail_func, fallback_func):
    def decorate(f):
        """
        circuit breaker decorator
        :param f
        :return:
        """

        @wraps(f)
        def wrapper(*args, **kwds):
            # Verify if the window parameter has been initialized
            if window is not None and callable(judge_fail_func) and callable(fallback_func):
                res = None
                # Check circuit breaker status
                if window.status == slidingwindow.CLOSE:
                    res = f(*args, **kwds)
                    if judge_fail_func(res):
                        if window.status == slidingwindow.HALF_OPEN:
                            res = fallback_func(*args, **kwds)
                        else:
                            window.increase_fail()
                    else:
                        if window.status == slidingwindow.HALF_OPEN:
                            window.status = slidingwindow.CLOSE
                elif window.status == slidingwindow.OPEN:
                    res = fallback_func(*args, **kwds)
                elif window.status == slidingwindow.HALF_OPEN:
                    if window.acquire_sem():
                        try:
                            res = f(*args, **kwds)
                            if judge_fail_func(res):
                                res = fallback_func(*args, **kwds)
                                window.set_open()
                            else:
                                window.status = slidingwindow.CLOSE
                        finally:
                            window.release_sem()
                    else:
                        res = fallback_func(*args, **kwds)
                return res
            logging.error('Circuit breaker is initialized failed!')
            return f(*args, **kwds)

        return wrapper

    return decorate


def initialize_circuit_breaker(rate=1000, period=10 * 1000, volume_threshold=20, sleep_window_in_milliseconds=5000,
                               step=1, threshold_percentage=0.5):
    """
    Initialize circuit breaker
    :param rate: The interval of checking health status, default is 1000ms
    :param period: How long the circuit breaker will be opened, default is 10*1000ms
    :param volume_threshold: The minimum sample size, default is 20
    :param sleep_window_in_milliseconds: The HALF OPEN status duration, default is 5000ms
    :param step: The counter's increased step size, default is 1
    :param threshold_percentage: The failure rate, default is 50%
    :return:
    """
    window = slidingwindow.SlidingWindow(rate, period, sleep_window_in_milliseconds, volume_threshold, step,
                                         threshold_percentage)
    window.start()
    return window
