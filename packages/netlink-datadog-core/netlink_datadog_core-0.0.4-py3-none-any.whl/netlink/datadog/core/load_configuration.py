import yaml
from netlink.logging import logger


def get_datadog_configuration():
    """Read file 'datadog.yaml' in <cwd>/conf.d"""
    logger.verbose("Reading Datadog configuration")
    with open("conf.d/datadog.yaml", "r", encoding="utf-8-sig") as f:
        datadog_configuration = yaml.safe_load(f)
    logger.trace(datadog_configuration)
    return datadog_configuration
