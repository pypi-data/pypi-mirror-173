# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spelunk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'spelunk',
    'version': '0.1.0',
    'description': 'Package with helpful object recursion utils',
    'long_description': None,
    'author': 'Spencer Tomarken',
    'author_email': 'stomarken@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
