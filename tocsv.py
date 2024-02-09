#!/usr/bin/env python
import argparse
from pathlib import Path
from datetime import datetime
import struct


def parser():
    p = argparse.ArgumentParser(prog=__name__)
    p.add_argument('binary_log', metavar='binary-log', type=Path, help='Path to binary log to convert')
    p.add_argument('-l', '--long-field', action='store_true', help='Use if value is UINT32 (otherwise UINT16 is used)')
    p.add_argument('-o', '--output', type=Path, help='output CSV file to log timestamp and value')
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    if args.output:
        out = args.output.open('w')
        out.write(f'time,value\n')
    with args.binary_log.open('rb') as blog:
        while True:
            tsb = blog.read(4)
            if not tsb:
                break
            ts = struct.unpack('>I', tsb)[0]
            ts = datetime.fromtimestamp(ts)
            if args.long_field:
                val = struct.unpack('>I', blog.read(4))[0]
            else:
                val = struct.unpack('>H', blog.read(2))[0]
            if args.output:
                out.write(f'{ts},{val}\n')
            print(f'{ts},{val}')
    if args.output:
        out.close()


if __name__ == '__main__':
    main()
