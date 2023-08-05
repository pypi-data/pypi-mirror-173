# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'combobox': 'src\\combobox',
 'date': 'src\\date',
 'date_partition': 'src\\date_partition',
 'store': 'src\\store'}

packages = \
['checkbox', 'combobox', 'date', 'date_partition', 'store']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'random-filters',
    'version': '1.4.3',
    'description': 'A package for generating random filters',
    'long_description': '',
    'author': 'Renan',
    'author_email': 'renancavalcantercb@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
