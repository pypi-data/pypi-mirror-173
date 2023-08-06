# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oonidata', 'oonidata.cli', 'oonidata.db']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'boto3>=1.24.2,<2.0.0',
 'clickhouse-driver>=0.2.3,<0.3.0',
 'cryptography>=38.0.2,<39.0.0',
 'dacite>=1.6.0,<2.0.0',
 'lxml>=4.9.0,<5.0.0',
 'lz4>=4.0.1,<5.0.0',
 'mashumaro>=3.0.4,<4.0.0',
 'maxminddb>=2.2.0,<3.0.0',
 'orjson>=3.8.0,<4.0.0',
 'py-radix>=0.10.0,<0.11.0',
 'pyOpenSSL>=22.1.0,<23.0.0',
 'requests>=2.27.1,<3.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'ujson>=5.3.0,<6.0.0']

setup_kwargs = {
    'name': 'oonidata',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Arturo Filastò',
    'author_email': 'arturo@filasto.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
