# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['core']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'datadog-api-client>=2.5.0,<3.0.0',
 'netlink-logging>=0.1.9,<0.2.0']

entry_points = \
{'console_scripts': ['validate_api_key = '
                     'netlink.datadog.core.validate_api_key:validate_api_key_cli']}

setup_kwargs = {
    'name': 'netlink-datadog-core',
    'version': '0.0.3',
    'description': 'Integration for Datadog (Core)',
    'long_description': '# netlink-datadog-core\n\nCore of Integration for Datadog\n\nProviding a wrapper of the [datadog-api-client](https://pypi.org/project/datadog-api-client/).\n\n# Utilities\n\n- validate_api_key\n\n# Classes\n\n## Metric\n\n### \\_\\_init\\_\\_\n\n  - `name` **str** - Name of metric\n  - `type` [MetricIntakeType](https://datadoghq.dev/datadog-api-client-ruby/DatadogAPIClient/V2/MetricIntakeType.html) \n  - `host` optional - **str** - will be added as resource type host\n  - `env`  **str** - Tag\n  - `source` **str** - Tag\n  - `service` **str** - Tag\n  - `tags` **set** - custom tags\n\n### metric\n\nReturns a [MetricSeries](https://datadoghq.dev/datadog-api-client-ruby/DatadogAPIClient/V2/MetricSeries.html)\n  \n  - `timestamp`\n  - `value`\n  - `tags` **set** - additional custom tags\n\n## GaugeMetric(Metric)\n\n### \\_\\_init\\_\\_\n\n  - `name` **str** - Name of metric\n  - `host` optional - **str** - will be added as resource type host\n  - `env`  **str** - Tag\n  - `source` **str** - Tag\n  - `service` **str** - Tag\n  - `tags` **set** - custom tags\n\n### metric\n\nReturns a [MetricSeries](https://datadoghq.dev/datadog-api-client-ruby/DatadogAPIClient/V2/MetricSeries.html)\n  \n  - `timestamp`\n  - `value`\n  - `tags` **set** - additional custom tags\n\n## Worker(threading.Thread)\n\nSends metrics to Datadog received in queue.\n\n### \\_\\_init\\_\\_\n\n  - `name_index` **int** used to create thread name\n  - `api_key` **str** Datadog api key\n  - `site` **str** Datadog site\n  - `queue` **queue.SimpleQueue**\n  - `shutdown_event` **threading.Event**\n  ',
    'author': 'Bernhard Radermacher',
    'author_email': 'bernhard.radermacher@netlink-consulting.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/netlink_python/netlink-datadog-core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
