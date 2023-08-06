# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rawxio']

package_data = \
{'': ['*']}

install_requires = \
['pandas']

setup_kwargs = {
    'name': 'rawxio',
    'version': '0.1.2',
    'description': 'Import/Export rawx',
    'long_description': 'None',
    'author': 'Statnett Datascience',
    'author_email': 'Datascience.Drift@Statnett.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/statnett/rawxio.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
