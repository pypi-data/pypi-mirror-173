from numbers import Real
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_resource import MetricResource
from datadog_api_client.v2.model.metric_series import MetricSeries

class Metric:
    name: str
    type: MetricIntakeType
    host: str
    tags: set
    kwargs: dict

    def __init__(
        self,
        name: str,
        type: MetricIntakeType,
        host: str = None,
        env: str = None,
        source: str = None,
        service: str = None,
        tags: set = None,
    ) -> None: ...
    def metric(self, timestamp: int, value: Real, tags: set = None) -> MetricSeries: ...

class GaugeMetric(Metric):
    def __init__(
        self, name: str, host: str = None, env: str = None, source: str = None, service: str = None, tags: set = None
    ) -> None: ...
