# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monitor', 'monitor.core', 'monitor.rfc', 'monitor.updater']

package_data = \
{'': ['*']}

install_requires = \
['netlink-core', 'netlink-logging']

setup_kwargs = {
    'name': 'netlink-sap-monitor',
    'version': '0.0.3',
    'description': 'SAP Monitoring',
    'long_description': '# netlink-sap-monitor\n\n## checks:\n\n- transactional_rfc_calls\n- updater_queue',
    'author': 'Bernhard Radermacher',
    'author_email': 'bernhard.radermacher@netlink-consulting.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/netlink_python/netlink-sap-monitor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
