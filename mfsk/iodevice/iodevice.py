#! /usr/bin/env python3

"""Generic IO device base classes"""

from abc import ABC, abstractmethod


class IODevice(ABC):
    """A generic I/O device"""

    @property
    @abstractmethod
    def sample_rate(self) -> int:
        """Sample rate (samples/sec)"""

    @abstractmethod
    def close(self) -> None:
        """Close the device"""


class ReaderDevice(IODevice):
    """A generic I/O input device"""

    @abstractmethod
    def read(self, samples: int) -> list[float]:
        """Read a block of n samples from a device.
           Samples are floating-point in the range [-1.0, 1.0]"""


class WriterDevice(IODevice):
    """A generic I/O output device"""

    @abstractmethod
    def write(self, data: list[float] | tuple[float]):
        """Write a block of samples to the device.
           Samples are floating-point in the range [-1.0, 1.0]"""
