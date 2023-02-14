#!/usr/bin/env python
import argparse
from pathlib import Path
from datetime import datetime
import struct
from snail.gql import proxied_client



def parser():
    p = argparse.ArgumentParser(prog=__name__)
    p.add_argument('-o', '--output', type=Path, help='output file to log timestamp and value')
    p.add_argument('--binary-log', action='store_true', help='Use binary format for log')
    return p


def main(argv=None):
    args = parser().parse_args(argv)

    client = proxied_client()
    pop = client.marketplace_count()
    print(f'Current population: {pop}')

    if args.output:
        now = datetime.utcnow()
        print(now)
        if args.binary_log:
            with args.output.open('ab') as f:
                f.write(struct.pack('>I', int(now.timestamp())))
                f.write(struct.pack('>H', pop))
        else:
            with args.output.open('a') as f:
                f.write(f'{now:%y-%m-%dT%H:%M:%S} {pop}\n')


if __name__ == '__main__':
    main()
