#! /usr/bin/env python3

"""Generic MFSK decoder"""

from math import sin, sqrt, pi

from .iodevice.iodevice import ReaderDevice


class Decoder:
    """Generic MFSK decoder"""

    def __init__(self,
                 frequencies: list[float] | tuple[float],
                 symbol_time: float,
                 input_device: ReaderDevice | None):
        self._frequencies = frequencies
        self._symbol_time = symbol_time
        self._input_device = input_device

        self._time = 0.0
        self._phase = 0.0

        self._symbol_size = int(self._input_device.sample_rate * self._symbol_time)
        self._symbol_offsets = [int(self._input_device.sample_rate / (4 * i)) for i in self._frequencies]

    def decode(self, symbol) -> int:
        """Decode a symbol."""

        magnitudes = []
        for offset in self._symbol_offsets:
            product = 1.0

            for i, q in zip(symbol[offset:], symbol):
                product *= sqrt((i**2) + (q**2))

            magnitudes.append(product)

        max_val = 0.0
        max_idx = 0
        for idx, val in enumerate(magnitudes):
            if val > max_val:
                max_val = val
                max_idx = idx

        return max_idx

    def decode_chunk(self, chunk) -> list[int]:
        """Decode a block of symbols"""

        ss = self._symbol_size

        return [self.decode(chunk[i*ss:i*(ss+1)]) for i in range(len(chunk) // ss)]

    def read(self) -> int:
        """Read a symbol from the output file"""

        if self._input_device is None:
            raise ValueError('Tried to read, but no input device was set!')

        chunk_data = self._input_device.read(self._symbol_size)

        return self.decode(chunk_data)

    def read_chunk(self, chunk_size) -> list[int]:
        """Read a block of symbols from the output file"""

        if self._input_device is None:
            raise ValueError('Tried to read, but no input device was set!')

        chunk_data = self._input_device.read(chunk_size * self._symbol_size)

        return self.decode_chunk(chunk_data)
