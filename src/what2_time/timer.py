from __future__ import annotations

from dataclasses import dataclass, field
from typing import Self, Callable, Any
import time
from what2_time.counter import TimeCounter


@dataclass
class BaseTimer:
    # todo: make repr nicer
    __start_time: int = field(default=0, init=False, repr=False)

    total_time: TimeCounter = field(default_factory=TimeCounter.nano_counter, init=True,kw_only=True)

    is_running: bool = field(default=False, init=False, repr=True)

    def start(self) -> Self:
        """Start a new timer"""
        self.__start_time = time.perf_counter_ns()
        self.is_running = True
        return self

    def as_seconds(self):
        return self.total_time.as_seconds()

    def stop(self) -> float:
        now = time.perf_counter_ns()
        elapsed = now - self.__start_time
        self.is_running = False
        self.total_time.add(elapsed)
        return self.as_seconds()

    def reset(self):
        self.total_time.reset()

    def __enter__(self) -> Self:
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info: Any) -> None:
        """Stop the context manager timer"""
        self.stop()


@dataclass
class Timer(BaseTimer):
    name: str | None = field(default=None, repr=True)
    logger: Callable[[str], Any] | None = field(default=print, repr=False)

    def stop(self) -> float:
        elapsed_time = super().stop()

        self.reset()
        if self.logger:
            # todo: units
            message = f'Elapsed time: {elapsed_time:0.4f} seconds'
            if self.name:
                message = f'{self.name} - {message}'

            self.logger(message)

        return elapsed_time


@dataclass
class MetaTimer(BaseTimer):
    name: str

    def __post_init__(self):
        self.total_time
