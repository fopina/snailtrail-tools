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
        for k, v in pop.items():
            pop_file = args.output.with_suffix(f'.{k}{args.output.suffix}')
            if args.binary_log:
                with pop_file.open('ab') as f:
                    f.write(struct.pack('>I', int(now.timestamp())))
                    f.write(struct.pack('>H', v))
            else:
                with pop_file.open('a') as f:
                    f.write(f'{now:%y-%m-%dT%H:%M:%S} {v}\n')


if __name__ == '__main__':
    main()
