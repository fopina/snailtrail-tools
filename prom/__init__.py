from prometheus_client import start_http_server, Gauge, CollectorRegistry
import time
import subprocess
from pathlib import Path

class HackedCollectorRegistry(CollectorRegistry):
    """
    modified registry class to have a callback on every collect
    """
    _cb = None

    def collect(self):
        yield from super().collect()
        if self._cb is not None:
            self._cb()

def push_metric(binary, url, username, password, metric_name, metric_description, value):
    registry = HackedCollectorRegistry(auto_describe=True)
    
    # Start up the server to expose the metrics.
    start_http_server(9100, registry=registry)
    
    g = Gauge(metric_name, metric_description, registry=registry)
    g.set(value)

    p = subprocess.Popen(
        [binary, '--config.expand-env', '--config.file', Path(__file__).parent / 'agent-config.yaml'],
        env={
            'PROM_URL': url,
            'PROM_USERNAME': username,
            'PROM_PASSWORD': password,
        }
    )

    stop = [False]
    def _a():
        p.terminate()
        stop[0] = True
    registry._cb = _a

    while not stop[0]:
        time.sleep(1)
