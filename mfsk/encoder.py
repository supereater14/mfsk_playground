#! /usr/bin/env python3

"""Generic MFSK encoder"""

from math import sin, pi

from .iodevice.iodevice import WriterDevice


class Encoder:
    """Generic MFSK encoder"""

    def __init__(self,
                 frequencies: list[float] | tuple[float],
                 symbol_time: float,
                 output_device: WriterDevice | None):
        self._frequencies = frequencies
        self._symbol_time = symbol_time
        self._output_device = output_device

        self._time = 0.0
        self._phase = 0.0
        self._steps = [(i * 2 * pi) / self._output_device.sample_rate
                       for i in self._frequencies]
        self._step_time = 1.0 / self._output_device.sample_rate

    def encode(self, symbol) -> list[float]:
        """Encode a symbol."""

        sample_chunk = []

        while self._time < self._symbol_time:
            self._phase += self._steps[symbol]
            sample_chunk.append(sin(self._phase))
            self._time += self._step_time
        self._time -= self._symbol_time

        return sample_chunk

    def encode_chunk(self, chunk) -> list[float]:
        """Encode a block of symbols"""

        encoded_chunk = []

        for symbol in chunk:
            encoded_chunk.extend(self.encode(symbol))

        return encoded_chunk

    def write(self, symbol) -> None:
        """Write a symbol to the output file"""

        if self._output_device is None:
            raise ValueError('Tried to write, but no output device was set!')

        chunk = self.encode(symbol)

        self._output_device.write(chunk)

    def write_chunk(self, chunk) -> None:
        """Write a block of symbols to the output file"""

        if self._output_device is None:
            raise ValueError('Tried to write, but no output device was set!')

        encoded_chunk = self.encode_chunk(chunk)

        self._output_device.write(encoded_chunk)
