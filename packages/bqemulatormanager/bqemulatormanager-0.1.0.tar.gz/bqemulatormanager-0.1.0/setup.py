# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bqemulatormanager']

package_data = \
{'': ['*']}

install_requires = \
['db-dtypes>=1.0.4,<2.0.0',
 'google-cloud-bigquery>=3.3.5,<4.0.0',
 'pandas>=1.5.1,<2.0.0',
 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'bqemulatormanager',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'gyuta',
    'author_email': 'kuroshiba0408@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
