import argparse
from functools import cached_property
from web3 import Web3
from web3.middleware import geth_poa_middleware
from pathlib import Path
from datetime import datetime, timezone


CONTRACT_INCUBATOR = '0x09457e0181dA074610530212A6378605382764b8'
ABI_INCUBATOR = [
    {
        'inputs': [],
        'name': 'getCurrentCoefficent',
        'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}],
        'stateMutability': 'view',
        'type': 'function',
    },
]

class Client:
    def __init__(
        self,
        wallet,
        web3_provider,
    ):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.wallet = wallet

    @cached_property
    def incubator_contract(self):
        return self.web3.eth.contract(address=self.web3.toChecksumAddress(CONTRACT_INCUBATOR), abi=ABI_INCUBATOR)

    def get_current_coefficent(self):
        return self.incubator_contract.functions.getCurrentCoefficent().call({'from': self.wallet})


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
