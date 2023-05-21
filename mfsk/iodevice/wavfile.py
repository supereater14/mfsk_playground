#! /usr/bin/env python3

"""WAV file reader/writer"""

import struct
import wave

from .iodevice import ReaderDevice, WriterDevice


class WavWriter(WriterDevice):
    """WAV file output device"""
    def __init__(self, file, samp_rate, samp_width: int = 2):
        self._samp_rate = samp_rate
        self._samp_width = samp_width

        self._bits = self._samp_width * 8

        struct_str_map = {1: 'b', 2: 'h', 4: 'i', 8: 'q'}
        if self._samp_width not in struct_str_map:
            raise ValueError('Invalid sample width')
        self._struct_str_base = f'{struct_str_map[self._samp_width]}'

        self._output_file = wave.open(file, 'wb')
        self._output_file.setnchannels(1)
        self._output_file.setsampwidth(self._samp_width)
        self._output_file.setframerate(self._samp_rate)

    def close(self):
        self._output_file.close()

    @property
    def sample_rate(self):
        return self._samp_rate

    def write(self, data):
        scaled = [int(i * ((2**(self._bits - 1)) - 1)) for i in data]

        struct_str = f'<{len(scaled)}{self._struct_str_base}'
        encoded = struct.pack(struct_str, *scaled)

        self._output_file.writeframes(encoded)


class WavReader(ReaderDevice):
    def __init__(self, file):
        self._input_file = wave.open(file, 'rb')

        samp_width = self._input_file.getsampwidth()
        struct_str_map = {1: 'b', 2: 'h', 4: 'i', 8: 'q'}
        if samp_width not in struct_str_map:
            raise ValueError('Invalid sample width')
        self._struct_str_base = f'{struct_str_map[samp_width]}'

    def close(self):
        self._input_file.close()

    @property
    def sample_rate(self):
        return self._input_file.getframerate()

    def read(self, samples: int) -> list[float]:
        data = self._input_file.readframes(samples)

        samp_width = self._input_file.getsampwidth()
        struct_str = f'<{len(data) // samp_width}{self._struct_str_base}'
        decoded = struct.unpack(struct_str, data)

        bits = samp_width * 8
        scaled = [i / ((2**(bits - 1)) - 1) for i in decoded]

        return scaled
