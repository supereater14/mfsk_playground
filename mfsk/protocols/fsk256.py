#! /usr/bin/env python3

"""FSK256 Experimental encoder."""

from ..decoder import Decoder as DecoderBase
from ..encoder import Encoder as EncoderBase
from ..iodevice.iodevice import ReaderDevice, WriterDevice


BAND_LOW = 300
BAND_HIGH = 5000
NTONES = 256
SYMBOL_TIME = 0.05

BANDWIDTH = BAND_HIGH - BAND_LOW
TONE_STEP = BANDWIDTH / NTONES
TONES = [(i * TONE_STEP) + BAND_LOW for i in range(NTONES)]


class Encoder(EncoderBase):
    def __init__(self, output_device: WriterDevice):
        super().__init__(TONES, SYMBOL_TIME, output_device)

class Decoder(DecoderBase):
    def __init__(self, input_device: ReaderDevice):
        super().__init__(TONES, SYMBOL_TIME, input_device)
