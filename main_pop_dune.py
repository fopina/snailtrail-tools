#!/usr/bin/env python
import argparse
from pathlib import Path
from datetime import datetime
import struct
import requests
import os
import json
import subprocess

QUERY_ID = 1248485


def parser():
    p = argparse.ArgumentParser(prog=__name__)
    p.add_argument('-o', '--output', type=Path, help='output file to log timestamp and value')
    p.add_argument('--binary-log', action='store_true', help='Use binary format for log')
    return p


def append_if_not_exists(pop_file, line):
    if pop_file.exists():
        # check if entry already exists
        with pop_file.open('rb') as file:
            file.seek(-len(line), os.SEEK_END)
            if line in file.read():
                return False
    with pop_file.open('ab') as f:
        f.write(line)
    return True


def main(argv=None):
    args = parser().parse_args(argv)

    # FIXME: temporary workaround with curl as dune seems to be blocking python-requests (JA3?)

    # r = requests.post(
    #     'https://core-hsr.dune.com/v1/graphql',
    #     headers={
    #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0',
    #     },
    #     json={
    #         "operationName": "GetResult",
    #         "variables": {"query_id": QUERY_ID, "parameters": []},
    #         "query": "query GetResult($query_id: Int!, $parameters: [Parameter!]!) {\n  get_result_v3(query_id: $query_id, parameters: $parameters) {\n    job_id\n    result_id\n    error_id\n    __typename\n  }\n}\n",
    #     },
    # )
    # r.raise_for_status()
    x = subprocess.check_output(
        [
            'curl',
            'https://core-hsr.dune.com/v1/graphql',
            '-sXPOST',
            '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0',
            '--data-raw',
            json.dumps({
                "operationName": "GetResult",
                "variables": {"query_id": QUERY_ID, "parameters": []},
                "query": "query GetResult($query_id: Int!, $parameters: [Parameter!]!) {\n  get_result_v3(query_id: $query_id, parameters: $parameters) {\n    job_id\n    result_id\n    error_id\n    __typename\n  }\n}\n",
            }),
        ],
        text=True,
    )
    #execution_id = r.json()['data']['get_result_v3']['result_id']
    execution_id = json.loads(x)['data']['get_result_v3']['result_id']
    print(f'Execution ID: {execution_id}')

    # r = requests.post(
    #     'https://app-api.dune.com/v1/graphql',
    #     json={
    #         "operationName": "GetExecution",
    #         "variables": {"execution_id": execution_id, "query_id": QUERY_ID, "parameters": []},
    #         "query": "query GetExecution($execution_id: String!, $query_id: Int!, $parameters: [Parameter!]!) {\n  get_execution(\n    execution_id: $execution_id\n    query_id: $query_id\n    parameters: $parameters\n  ) {\n    execution_queued {\n      execution_id\n      execution_user_id\n      position\n      execution_type\n      created_at\n      __typename\n    }\n    execution_running {\n      execution_id\n      execution_user_id\n      execution_type\n      started_at\n      created_at\n      __typename\n    }\n    execution_succeeded {\n      execution_id\n      runtime_seconds\n      generated_at\n      columns\n      data\n      __typename\n    }\n    execution_failed {\n      execution_id\n      type\n      message\n      metadata {\n        line\n        column\n        hint\n        __typename\n      }\n      runtime_seconds\n      generated_at\n      __typename\n    }\n    __typename\n  }\n}\n",
    #     },
    # )
    # r.raise_for_status()
    x = subprocess.check_output(
        [
            'curl',
            'https://app-api.dune.com/v1/graphql',
            '-sXPOST',
            '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0',
            '-H', 'content-type: application/json',
            '--data-raw',
            json.dumps({
                "operationName": "GetExecution",
                "variables": {"execution_id": execution_id, "query_id": QUERY_ID, "parameters": []},
                "query": "query GetExecution($execution_id: String!, $query_id: Int!, $parameters: [Parameter!]!) {\n  get_execution(\n    execution_id: $execution_id\n    query_id: $query_id\n    parameters: $parameters\n  ) {\n    execution_queued {\n      execution_id\n      execution_user_id\n      position\n      execution_type\n      created_at\n      __typename\n    }\n    execution_running {\n      execution_id\n      execution_user_id\n      execution_type\n      started_at\n      created_at\n      __typename\n    }\n    execution_succeeded {\n      execution_id\n      runtime_seconds\n      generated_at\n      columns\n      data\n      __typename\n    }\n    execution_failed {\n      execution_id\n      type\n      message\n      metadata {\n        line\n        column\n        hint\n        __typename\n      }\n      runtime_seconds\n      generated_at\n      __typename\n    }\n    __typename\n  }\n}\n",
            }),
        ],
        text=True,
    )
    # data = r.json()['data']
    data = json.loads(x)['data']
    holders = data['get_execution']['execution_succeeded']['data']
    timestamp = data['get_execution']['execution_succeeded']['generated_at']
    print(f'Execution {execution_id} from {timestamp}')
    assert timestamp[-1] == 'Z'

    other = 0
    workers = 0
    burnt = 0
    for d in holders:
        if 'Workers(Sink) Contract' in d['holder']:
            workers = d['total_amount']
        elif 'Graveyard' in d['holder']:
            burnt = d['total_amount']
        else:
            other += d['total_amount']
    # FIXME: dune reports ~130 more of alive snails than the API - what snails are these?!
    pop = {'alive': other + workers, 'dead': burnt, 'working': workers}
    print(f'Current population: {pop}')

    if args.output:
        now = datetime.fromisoformat(timestamp.split('.')[0])
        print(now)
        for k, v in pop.items():
            pop_file: Path = args.output.with_suffix(f'.{k}{args.output.suffix}')
            if args.binary_log:
                if not append_if_not_exists(
                    pop_file,
                    struct.pack('>I', int(now.timestamp())) + struct.pack('>H', v),
                ):
                    print(f'{k} already has this point')
            else:
                if not append_if_not_exists(
                    pop_file,
                    f'{now:%y-%m-%dT%H:%M:%S} {v}\n'.encode(),
                ):
                    print(f'{k} already has this point')


if __name__ == '__main__':
    main()
