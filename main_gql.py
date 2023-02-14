#!/usr/bin/env python
import argparse
from pathlib import Path
import requests
import subprocess
import atexit
import datetime
import struct


GQL_MARKETPLACE = '''
query getAllSnail {
  marketplace_promise {
    ... on Snails {
    count  
    }
  }
}
'''

class Client(requests.Session):
    def __init__(self, url):
        super().__init__()
        self.url = url
    
    def query(self, operation, variables, query):
        r = self.post(
            self.url,
            json={
                'operationName': operation,
                'variables': variables,
                'query': query,
            },
        )
        r.raise_for_status()
        r = r.json()
        if r.get('data') is None:
            raise Exception(r)
        problems = [v['problem'] for v in r['data'].values() if 'problem' in v]
        if problems:
            raise Exception(problems)
        return r["data"]

    def marketplace_count(self):
        return int(self.query('getAllSnail', {}, GQL_MARKETPLACE)['marketplace_promise']['count'])


def parser():
    p = argparse.ArgumentParser(prog=__name__)
    p.add_argument('-o', '--output', type=Path, help='output file to log timestamp and value')
    p.add_argument('--binary-log', action='store_true', help='Use binary format for log')
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    c_id = subprocess.check_output('docker run --rm -dp 9999:8888 fopina/random:snailtrail-gotls', shell=True, text=True)
    atexit.register(lambda: subprocess.check_output(['docker', 'kill', c_id.strip()]))

    client = Client('http://127.0.0.1:9999/graphql')
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
