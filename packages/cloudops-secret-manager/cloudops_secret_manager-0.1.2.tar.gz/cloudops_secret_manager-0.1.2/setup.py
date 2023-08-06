# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloudops', 'cloudops.secret_manager']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0']

setup_kwargs = {
    'name': 'cloudops-secret-manager',
    'version': '0.1.2',
    'description': 'The cloudops-secret-manager package',
    'long_description': '# Cloudops Secret Manager\n\nBasic definitions for Secret Management\n',
    'author': 'Manuel Castillo',
    'author_email': 'manucalop@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/manucalop/cloudops-secret-manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
