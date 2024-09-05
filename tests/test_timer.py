import time

from what2 import dbg
from what2_time import MetaTimer, Timer
from what2_time.counter import TimeCounter

from _pytest.python_api import ApproxScalar


def approx(val: float) -> ApproxScalar:
    return ApproxScalar(
        expected=val,
        rel=0.01,
    )


def test_time_counter_counts_second():
    counter = TimeCounter.nano_counter()
    counter.add(TimeCounter.nanosecond_base)
    counted = counter.as_seconds()
    assert counted == 1


def test_single_second_timer():
    duration = 1
    t = Timer().start()
    time.sleep(duration)
    elapsed = t.stop()
    dbg(elapsed)
    assert elapsed == approx(duration)


def test_simple_meta():
    with MetaTimer("metaT"):
        time.sleep(1)
    elapsed = MetaTimer.get_meta_duration("metaT")
    assert elapsed == approx(1)

    with MetaTimer("metaT"):
        time.sleep(1)
    elapsed = MetaTimer.get_meta_duration("metaT")
    assert elapsed == approx(2)
