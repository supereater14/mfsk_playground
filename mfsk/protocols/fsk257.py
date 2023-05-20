#! /usr/bin/env python3

"""FSK257 Experimental encoder."""

from ..encoder import Encoder as EncoderBase
from ..iodevice.iodevice import WriterDevice


BAND_LOW = 300
BAND_HIGH = 5000
NTONES = 257
SYMBOL_TIME = 0.05

BANDWIDTH = BAND_HIGH - BAND_LOW
TONE_STEP = BANDWIDTH / NTONES
TONES = [(i * TONE_STEP) + BAND_LOW for i in range(NTONES)]


class Encoder(EncoderBase):
    def __init__(self, output_device: WriterDevice):
        super().__init__(TONES, SYMBOL_TIME, output_device)

        self._last_symbol = -1

    def encode(self, symbol):
        if symbol == self._last_symbol:
            symbol = 256

        self._last_symbol = symbol

        return super().encode(symbol)
