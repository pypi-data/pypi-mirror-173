# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['core']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'datadog-api-client>=2.4.0,<3.0.0',
 'netlink-logging>=0.1.9,<0.2.0']

entry_points = \
{'console_scripts': ['validate_api_key = '
                     'netlink.datadog.core.validate_api_key:validate_api_key_cli']}

setup_kwargs = {
    'name': 'netlink-datadog-core',
    'version': '0.0.1',
    'description': 'Integration for Datadog (Core)',
    'long_description': '# netlink-datadog-core\n\nCore of Integration for Datadog\n\n',
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
