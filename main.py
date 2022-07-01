import argparse
from pathlib import Path
from datetime import datetime, timezone

from snail import Client


def parser():
    p = argparse.ArgumentParser(prog=__name__)
    p.add_argument('wallet')
    p.add_argument('avax_rpc_url')
    p.add_argument('-o', '--output', type=Path, help='output file to log timestamp and value')
    p.add_argument(
        '-p',
        '--prom',
        nargs=4,
        metavar=('grafana_agent_bin', 'remote_write_url', 'username', 'password'),
        help='push metrics to Prometheus (using Grafana Agent)',
    )
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
    if args.prom:
        import prom

        prom.push_metric(
            args.prom[0],
            args.prom[1],
            args.prom[2],
            args.prom[3],
            'my_inprogress_tests',
            'Something',
            c,
        )


if __name__ == '__main__':
    main()
