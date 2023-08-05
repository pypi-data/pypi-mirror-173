# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flakow1stprojetcc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'flakow1stprojetcc',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'flakow',
    'author_email': 'tonyimportsmg@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
