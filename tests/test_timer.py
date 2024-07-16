from what2_time import Timer
from what2_time.timer import TimeCounter
from what2 import dbg
import time


def is_approx(val: float, target: float):
    return abs(val - target) < 0.1


def test_time_counter_counts_second():
    counter = TimeCounter.nano_counter()
    counter.add(TimeCounter.nanosecond_base)
    counted = counter.as_seconds()
    assert counted == 1


def test_single_second_timer():
    t = Timer().start()
    time.sleep(1)
    elapsed = t.stop()
    dbg(elapsed)
    assert is_approx(elapsed, 1)
