import time

from what2 import dbg
from what2_time import MetaTimer, Timer
from what2_time.counter import TimeCounter


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


def test_simple_meta():
    with MetaTimer("metaT"):
        time.sleep(1)
    elapsed = MetaTimer.get_meta_duration("metaT")
    assert is_approx(elapsed, 1)

    with MetaTimer("metaT"):
        time.sleep(1)
    elapsed = MetaTimer.get_meta_duration("metaT")
    assert is_approx(elapsed, 2)
