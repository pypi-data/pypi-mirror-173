# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wrps']

package_data = \
{'': ['*']}

install_requires = \
['watchfiles>=0.18.0,<0.19.0']

setup_kwargs = {
    'name': 'wrps',
    'version': '0.1.0',
    'description': 'A simple Python script reloader',
    'long_description': None,
    'author': 'megahomyak',
    'author_email': 'g.megahomyak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
