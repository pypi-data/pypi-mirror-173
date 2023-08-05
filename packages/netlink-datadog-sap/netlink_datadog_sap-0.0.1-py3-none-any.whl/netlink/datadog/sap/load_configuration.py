import yaml
from netlink.logging import logger


def get_abap_configuration():
    """Read file 'abap.yaml' in <cwd>/conf.d"""
    logger.verbose("Reading ABAP configuration")
    with open("conf.d/abap.yaml", "r", encoding="utf-8-sig") as f:
        abap_configuration = yaml.safe_load(f)
    logger.trace(abap_configuration)
    return abap_configuration
