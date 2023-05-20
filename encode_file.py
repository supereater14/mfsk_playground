#! /usr/bin/env python3

import argparse

from mfsk.protocols.fsk256 import FSK256Encoder
from mfsk.iodevice.wavfile import WavWriter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    args = parser.parse_args()

    with open(args.input_file, 'rb') as input_file:
        data = input_file.read()

    output_device = WavWriter(args.output_file, samp_rate=48000)
    encoder = FSK256Encoder(output_device)
    encoder.write_chunk(data)
    output_device.close()

if __name__ == '__main__':
    main()
