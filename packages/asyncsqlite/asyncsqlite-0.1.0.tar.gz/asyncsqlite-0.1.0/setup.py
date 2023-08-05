# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncsqlite']

package_data = \
{'': ['*']}

install_requires = \
['aiosqlite>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'asyncsqlite',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Snowie-ORG/asyncsqlite',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
