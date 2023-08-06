from datetime import datetime
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_resource import MetricResource
from datadog_api_client.v2.model.metric_series import MetricSeries

from netlink.logging import logger


class Metric:
    def __init__(self, name, type, host=None, env=None, source=None, service=None, tags=None):
        logger.debug(f"Initializing metric {name}")
        logger.trace(f"type: {type}, host: {host}, env: {env}, source: {source}, service: {service}, tags: {tags}")
        self.name = name
        self.type = type
        self.host = host
        self.tags = set()
        if env:
            self.tags.add(f"env:{env}")
        if source:
            self.tags.add(f"source:{source}")
        if service:
            self.tags.add(f"service:{service}")
        self.tags = self.tags.union(tags or set())
        self.kwargs = dict(metric=self.name, type=self.type)
        if self.host:
            self.kwargs["resources"] = [MetricResource(name=self.host, type="host")]

    def metric(self, timestamp, value, tags=None):
        logger.debug(
            f'Metric {self.name}: {value} at {datetime.fromtimestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%SZ")}'
        )
        kwargs = self.kwargs.copy()
        tags = self.tags.union(tags or set())
        if tags:
            logger.trace("Tags: " + ", ".join(tags))
            kwargs["tags"] = list(tags)
        return MetricSeries(
            points=[
                MetricPoint(timestamp=timestamp, value=value),
            ],
            **kwargs,
        )


class GaugeMetric(Metric):
    def __init__(self, name, host=None, env=None, source=None, service=None, tags=None):
        super(GaugeMetric, self).__init__(name, MetricIntakeType.GAUGE, host, env, source, service, tags)
