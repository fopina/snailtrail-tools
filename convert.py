#!/usr/bin/env python

from pathlib import Path
from datetime import datetime
import struct


def main():
    with Path('log.txt').open('r') as inp, Path('log.bin').open('wb') as out:
        for l in inp:
            l = l.strip()
            datestr, coef = l.split(' ')
            _date = datetime.strptime(datestr, '%y-%m-%dT%H:%M:%S')
            coef = int(coef)
            seconds = int(_date.timestamp())
            out.write(struct.pack('>I', seconds))
            # assume coefficent always under 65% (<=65535) to save some bytes!
            out.write(struct.pack('>H', coef))


if __name__ == '__main__':
    main()
