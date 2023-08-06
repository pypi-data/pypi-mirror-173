# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bqemulatormanager']

package_data = \
{'': ['*']}

install_requires = \
['db-dtypes>=1.0.4,<2.0.0', 'google-cloud-bigquery==2.34.4', 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'bqemulatormanager',
    'version': '0.1.6',
    'description': '',
    'long_description': "# BiqQueryEmulator Manager\n\n\nthis package is wrapper of [bigquery-emulator](https://github.com/goccy/bigquery-emulator) which provides us BigQuery mock working in local machine.\n\nusing this package, you can\n\n- do unit test of your sql\n- download the schema of big query, and use it to make test data\n\n## usage\n1. following [instruction](https://github.com/goccy/bigquery-emulator#install),  download `bigquery-emulator` command.\n\n2. install this package. \n```\npip install bqemulatormanager\n```\n\n3. test your sql.\n```python\nimport bqemulatormanager as bqem\nimport pandas as pd\n\nmanager = bqem.Manager(project='test', schema_path='resources/schema_example.yaml')\n\nwith manager:\n    data = pd.DataFrame([\n        {'id': 1, 'name': 'sato'},\n        {'id': 2, 'name': 'yamada'}\n    ])\n\n    manager.load(data, 'dataset1.table_a')\n\n    sql = 'SELECT id, name FROM `dataset1.table_a`'\n\n    df = manager.query(sql)\nprint(df)\n```\n\n### automatically detect schema\nWhen called `Manager.load`, `SchemaManager` search correspond table schema from `schema_path` (default is `master_schema.yaml`).\n\nIf schema definition canot be found, `SchemaManager` request it from BigQuery in production environmant and update master schema file.",
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
