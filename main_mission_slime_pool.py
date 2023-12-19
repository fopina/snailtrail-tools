import argparse
from pathlib import Path
from datetime import datetime
import struct
from snail import Client

MISSION_TREASURY = '0x450324d8C9a7AbF3B1626D590cf4Beb48366D3B8'

def parser():
    p = argparse.ArgumentParser(prog=__name__)
    p.add_argument('avax_rpc_url')
    p.add_argument('-o', '--output', type=Path, help='output file to log timestamp and value')
    p.add_argument('--binary-log', action='store_true', help='Use binary format for log')
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    web3 = Client(MISSION_TREASURY, args.avax_rpc_url)
    c = web3.balance_of(MISSION_TREASURY) / 10**18
    print(f'Current slime balance: {c}')
    if args.output:
        c = int(c)
        now = datetime.utcnow()
        print(now)
        if args.binary_log:
            with args.output.open('ab') as f:
                f.write(struct.pack('>I', int(now.timestamp())))
                f.write(struct.pack('>I', c))
        else:
            with args.output.open('a') as f:
                f.write(f'{now:%y-%m-%dT%H:%M:%S} {c}\n')


if __name__ == '__main__':
    main()
