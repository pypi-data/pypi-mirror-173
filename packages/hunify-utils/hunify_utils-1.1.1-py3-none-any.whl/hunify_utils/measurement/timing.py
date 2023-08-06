from time import perf_counter

__handlers = dict()


def start(handler: int = 0):
    __handlers[handler] = perf_counter()


def stop(handler: int = 0) -> float:
    __counter_value = perf_counter()
    return __counter_value - __handlers.get(handler, __counter_value)
