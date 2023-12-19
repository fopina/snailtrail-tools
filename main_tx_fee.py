import argparse
from pathlib import Path
from datetime import datetime
import struct
from snail import Client


def parser():
    p = argparse.ArgumentParser(prog=__name__)
    p.add_argument('avax_rpc_url')
    p.add_argument('-o', '--output', type=Path, help='output file to log timestamp and value')
    p.add_argument('--binary-log', action='store_true', help='Use binary format for log')
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    web3 = Client('', args.avax_rpc_url)
    # in nAVAX
    c = web3.web3.eth.gas_price / 10**9
    print(f'Median tx fee (nAVAX): {c }')
    if args.output:
        c = int(c)
        now = datetime.utcnow()
        print(now)
        if args.binary_log:
            with args.output.open('ab') as f:
                f.write(struct.pack('>I', int(now.timestamp())))
                # assume coefficent always under 65% (<=65535) to save some bytes!
                f.write(struct.pack('>H', c))
        else:
            with args.output.open('a') as f:
                f.write(f'{now:%y-%m-%dT%H:%M:%S} {c}\n')


if __name__ == '__main__':
    main()
