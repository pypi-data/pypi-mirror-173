import threading
import time
import queue

from datadog_api_client import Configuration, ApiClient
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_payload import MetricPayload
from netlink.logging import logger


class DatadogWorker(threading.Thread):
    def __init__(self, name_index, api_key, site, queue, shutdown_event, *args, **kwargs):
        # noinspection PySuperArguments
        super(DatadogWorker, self).__init__(name=f"datadog-{name_index}", daemon=True, *args, **kwargs)
        self.api_key = api_key
        self.site = site
        self.queue = queue
        self.shutdown_event = shutdown_event

    def run(self):
        logger.debug(f"Starting Datadog worker {self.name} ({self.native_id})")
        configuration = Configuration(api_key=dict(apiKeyAuth=self.api_key), server_variables=dict(site=self.site))
        items = []
        send_now = False
        while not self.shutdown_event.is_set():
            try:
                items.append(self.queue.get(timeout=1))
            except queue.Empty:
                send_now = True
            if len(items) >= 100 or send_now:
                if items:
                    logger.debug(f"Sending {len(items)} items to Datadog")
                    with ApiClient(configuration) as api_client:
                        try:
                            response = MetricsApi(api_client).submit_metrics(body=MetricPayload(series=items))
                            if response.errors:
                                for i in response.errors:
                                    logger.error(i)
                        except Exception as e:
                            logger.error(f"{e.args}")
                            logger.debug(f"putting {len(items)} back -- queue length before {self.queue.qsize()}")
                            for item in items:
                                self.queue.put(item)
                            logger.debug(f"queue length after {self.queue.qsize()}")
                            time.sleep(10)
                        items.clear()
                send_now = False
