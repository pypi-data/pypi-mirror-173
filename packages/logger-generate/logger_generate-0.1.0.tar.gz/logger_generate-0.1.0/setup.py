# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logger_generate']

package_data = \
{'': ['*']}

install_requires = \
['coloredlogs>=15.0.1,<16.0.0']

setup_kwargs = {
    'name': 'logger-generate',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'we684123',
    'author_email': 'we684123@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
