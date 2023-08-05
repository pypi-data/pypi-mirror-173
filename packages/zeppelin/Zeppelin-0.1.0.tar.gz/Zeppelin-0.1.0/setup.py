# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zeppelin', 'zeppelin.data_models', 'zeppelin.data_sources']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zeppelin',
    'version': '0.1.0',
    'description': 'The package for easy configuration',
    'long_description': None,
    'author': 'altroncode',
    'author_email': 'cosmosx1328@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
