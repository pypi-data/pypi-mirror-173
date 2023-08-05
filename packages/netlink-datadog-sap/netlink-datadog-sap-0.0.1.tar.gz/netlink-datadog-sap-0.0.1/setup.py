# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sap', 'sap.abap']

package_data = \
{'': ['*']}

install_requires = \
['netlink-datadog-core>=0.0.2,<0.0.3',
 'netlink-sap-monitor>=0.0.1,<0.0.2',
 'netlink-sap-rfc>=0.1.16,<0.2.0',
 'schedule>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['datadog_sap_monitor = '
                     'netlink.datadog.sap.cli:datadog_sap_cli']}

setup_kwargs = {
    'name': 'netlink-datadog-sap',
    'version': '0.0.1',
    'description': 'Integration for Datadog (SAP)',
    'long_description': '# netlink-datadog-sap\n\nIntegration of information retrieved from netlink-sap-monitor to Datadog.\n\n## Changes\n\n### 0.0.1\n\n- rfc_transactional_calls',
    'author': 'Bernhard Radermacher',
    'author_email': 'bernhard.radermacher@netlink-consulting.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/netlink_python/netlink-datadog-sap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
