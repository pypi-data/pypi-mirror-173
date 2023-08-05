import click
from netlink.datadog.core import get_datadog_configuration
from .load_configuration import get_abap_configuration
from .datadog_sap import DatadogSapMonitor

from netlink.logging import logger


@click.command()
def datadog_sap_cli():
    logger.set_level(logger.DEBUG)
    logger.set_file("datadog_sap_monitor.log", log_level=logger.TRACE)

    monitor = DatadogSapMonitor(get_datadog_configuration(), get_abap_configuration())
    monitor.start()
