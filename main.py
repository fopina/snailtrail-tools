import argparse
from pathlib import Path
from datetime import datetime, timezone

from snail import Client


def parser():
    p = argparse.ArgumentParser(prog=__name__)
    p.add_argument('wallet')
    p.add_argument('avax_rpc_url')
    p.add_argument('-o', '--output', type=Path, help='output file to log timestamp and value')
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    web3 = Client(args.wallet, args.avax_rpc_url)
    c = web3.get_current_coefficent()
    # lower precision, save bytes
    # 1000000000000000000
    c = int(c / 1000000000000000)
    print(f'Current coefficent: {c / 1000}')
    if args.output:
        now = datetime.now(tz=timezone.utc)
        print(now)
        with args.output.open('a') as f:
            f.write(f'{now:%y-%m-%dT%H:%M:%S} {c}\n')


if __name__ == '__main__':
    main()
