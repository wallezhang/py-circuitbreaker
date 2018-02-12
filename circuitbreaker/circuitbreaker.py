# -*- coding: utf-8 -*-

import logging
from functools import wraps

import slidingwindow


def circuit_breaker(window, judge_fail_func, fallback_func):
    def decorate(f):
        """
        熔断装饰器
        :param f: 原始函数
        :return:
        """

        @wraps(f)
        def wrapper(*args, **kwds):
            # 验证是否初始化window变量
            if window is not None and callable(judge_fail_func) and callable(fallback_func):
                res = None
                # 检查熔断器状态
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
            logging.error('熔断器初始化失败！')
            return f(*args, **kwds)

        return wrapper

    return decorate


def initialize_circuit_breaker(rate=1000, period=10 * 1000, volume_threshold=20, sleep_window_in_milliseconds=5000,
                               step=1, threshold_percentage=0.5):
    """
    初始化熔断器
    :param rate: 速率，检查健康状态的时间间隔，单位：毫秒，默认1000
    :param period: 周期，多久内的失败率会导致熔断发生，单位：毫秒，默认10*1000
    :param volume_threshold: 采集周期内的样本最少数量，默认20
    :param sleep_window_in_milliseconds: 熔断半开的时间间隔，单位：毫秒，默认5000
    :param step: 增长步长
    :param threshold_percentage: 触发熔断的失败率，默认50%
    :return:
    """
    window = slidingwindow.SlidingWindow(rate, period, sleep_window_in_milliseconds, volume_threshold, step,
                                         threshold_percentage)
    window.start()
    return window
