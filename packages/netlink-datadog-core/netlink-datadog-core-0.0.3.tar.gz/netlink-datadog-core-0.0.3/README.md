# netlink-datadog-core

Core of Integration for Datadog

Providing a wrapper of the [datadog-api-client](https://pypi.org/project/datadog-api-client/).

# Utilities

- validate_api_key

# Classes

## Metric

### \_\_init\_\_

  - `name` **str** - Name of metric
  - `type` [MetricIntakeType](https://datadoghq.dev/datadog-api-client-ruby/DatadogAPIClient/V2/MetricIntakeType.html) 
  - `host` optional - **str** - will be added as resource type host
  - `env`  **str** - Tag
  - `source` **str** - Tag
  - `service` **str** - Tag
  - `tags` **set** - custom tags

### metric

Returns a [MetricSeries](https://datadoghq.dev/datadog-api-client-ruby/DatadogAPIClient/V2/MetricSeries.html)
  
  - `timestamp`
  - `value`
  - `tags` **set** - additional custom tags

## GaugeMetric(Metric)

### \_\_init\_\_

  - `name` **str** - Name of metric
  - `host` optional - **str** - will be added as resource type host
  - `env`  **str** - Tag
  - `source` **str** - Tag
  - `service` **str** - Tag
  - `tags` **set** - custom tags

### metric

Returns a [MetricSeries](https://datadoghq.dev/datadog-api-client-ruby/DatadogAPIClient/V2/MetricSeries.html)
  
  - `timestamp`
  - `value`
  - `tags` **set** - additional custom tags

## Worker(threading.Thread)

Sends metrics to Datadog received in queue.

### \_\_init\_\_

  - `name_index` **int** used to create thread name
  - `api_key` **str** Datadog api key
  - `site` **str** Datadog site
  - `queue` **queue.SimpleQueue**
  - `shutdown_event` **threading.Event**
  