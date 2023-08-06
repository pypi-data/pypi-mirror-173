# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloudops', 'cloudops.secret_manager', 'cloudops.secret_manager.google']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-secret-manager>=2.11.0,<3.0.0', 'google-crc32c>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'cloudops-secret-manager-google',
    'version': '0.1.0',
    'description': 'The cloudops-secret-manager-google package',
    'long_description': '# cloudops-secret-manager-google\n',
    'author': 'Manuel Castillo',
    'author_email': 'manucalop@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/manucalop/cloudops-secret-manager-google',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
