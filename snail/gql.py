import requests
import subprocess
import atexit

# status: 3 means "alive and not working"
# no status == 3 + 5
GQL_MARKETPLACE = '''
query getAllSnail {
  alive: marketplace_promise {
    ... on Problem {
        problem
    }
    ... on Snails {
        count  
    }
  }
  dead: marketplace_promise(filters: {status: 4}) {
    ... on Problem {
        problem
    }
    ... on Snails {
        count  
    }
  }
  working: marketplace_promise(filters: {status: 5}) {
    ... on Problem {
        problem
    }
    ... on Snails {
        count  
    }
  }
}
'''

GQL_BURN = '''
query microwave_promise($params: MicrowaveParams) {
    microwave_promise(params: $params) {
        ... on Problem {
            problem
        }
        ... on GenericResponse {
            payload {
                ... on MicrowavePayload {
                    coef
                }
            }
        }
    }
}
'''


class Client(requests.Session):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def query(self, operation, variables, query, auth=None):
        kw = {}
        if auth:
            kw['headers'] = {'Auth': auth}
        r = self.post(
            self.url,
            json={
                'operationName': operation,
                'variables': variables,
                'query': query,
            },
            **kw,
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
        x = self.query('getAllSnail', {}, GQL_MARKETPLACE)
        return {k: v['count'] for k, v in x.items()}

    def burn_coef(self, token_id: int, signature: str, address: str, auth: str):
        return self.query(
            'microwave_promise',
            {'params': {'token_ids': [token_id], 'signature': signature, 'address': address, 'use_scroll': False}},
            GQL_BURN,
            auth=auth,
        )['microwave_promise']['payload']['coef']


def proxied_client():
    c_id = subprocess.check_output(
        [
            'docker',
            'run',
            '--rm',
            '-dp',
            '9999:8888',
            'ghcr.io/fopina/gotlsproxy:0.2',
            '-bind',
            '0.0.0.0:8888',
            '-ja3',
            '771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-21,29-23-24,0',
            '-ua',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'https://api.snailtrail.art/graphql/',
        ],
        text=True,
    ).strip()
    atexit.register(lambda: subprocess.check_output(['docker', 'kill', c_id]))
    subprocess.check_output(['docker', 'inspect', '--format={{.State.ExitCode}}', c_id], text=True)
    return Client('http://127.0.0.1:9999/graphql')
