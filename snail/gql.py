import requests
import subprocess
import atexit

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


def proxied_client():
    c_id = subprocess.check_output(['docker', 'run', '--rm', '-dp', '9999:8888', 'fopina/random:snailtrail-gotls'], text=True)
    atexit.register(lambda: subprocess.check_output(['docker', 'kill', c_id.strip()]))
    return Client('http://127.0.0.1:9999/graphql')
