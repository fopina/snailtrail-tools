#!/usr/bin/env python
import argparse
from pathlib import Path
from datetime import datetime
import struct
from snail.gql import proxied_client



def parser():
    p = argparse.ArgumentParser(prog=__name__)
    p.add_argument('token_id', type=int)
    p.add_argument('signature')
    p.add_argument('address')
    p.add_argument('auth')
    p.add_argument('-o', '--output', type=Path, help='output file to log timestamp and value')
    p.add_argument('--binary-log', action='store_true', help='Use binary format for log')
    return p


def main(argv=None):
    args = parser().parse_args(argv)

    client = proxied_client()
    coef = client.burn_coef(args.token_id, args.signature, args.address, args.auth)
    print(f'Current burn coeficient: {coef}')
    coef = int(coef * 1000)

    if args.output:
        now = datetime.utcnow()
        print(now)
        if args.binary_log:
            with args.output.open('ab') as f:
                f.write(struct.pack('>I', int(now.timestamp())))
                f.write(struct.pack('>I', coef))
        else:
            with args.output.open('a') as f:
                f.write(f'{now:%y-%m-%dT%H:%M:%S} {coef}\n')


if __name__ == '__main__':
    main()
