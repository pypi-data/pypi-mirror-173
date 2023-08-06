import threading
import queue

from datadog_api_client.v2.model.metric_series import MetricSeries

class Worker(threading.Thread):
    api_key: str
    site: str
    queue: queue.SimpleQueue
    shutdown_event: threading.Event

    def __init__(
        self,
        name_index: int,
        api_key: str,
        site: str,
        queue: queue.SimpleQueue,
        shutdown_event: threading.Event,
        *args,
        **kwargs,
    ) -> None: ...
    def run(self):
        items: list[MetricSeries]
