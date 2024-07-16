from dataclasses import dataclass, field
from typing import ClassVar, Self
from functools import partialmethod


@dataclass
class TimeCounter:
    base: int
    count: int = field(default=0, init=False)

    second_base: ClassVar[int] = 1
    millisecond_base: ClassVar[int] = 1000
    microsecond_base: ClassVar[int] = 1000000
    nanosecond_base: ClassVar[int] = 1000000000

    @classmethod
    def nano_counter(cls) -> Self:
        return cls(base=TimeCounter.nanosecond_base)

    @classmethod
    def second_counter(cls) -> Self:
        return cls(base=TimeCounter.second_base)

    def as_unit(self, base: int) -> float:
        if base == self.base:
            return self.count
        return (self.count * base) / self.base

    as_seconds = partialmethod(as_unit, second_base)
    as_milli = partialmethod(as_unit, millisecond_base)
    as_micro = partialmethod(as_unit, microsecond_base)
    as_nano = partialmethod(as_unit, nanosecond_base)

    def add(self, other: int):
        self.count += other

    def add_timer(self, other: TimeCounter):
        if self.base == other.base:
            self.count += other.count
            return

        self.count += int(other.as_unit(self.base))

    def add_unsafe_timer(self, other: TimeCounter):
        self.count += other.count

    def reset(self) -> None:
        self.count = 0

    def __lt__(self, other: TimeCounter) -> bool:
        return self.as_nano() < other.as_nano()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TimeCounter):
            return False
        return self.as_nano() == other.as_nano()
