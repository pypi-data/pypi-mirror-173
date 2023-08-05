# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_slapdash']

package_data = \
{'': ['*']}

install_requires = \
['boto3-stubs>=1.24.89,<2.0.0', 'boto3>=1.24.89,<2.0.0']

setup_kwargs = {
    'name': 'aws-slapdash',
    'version': '0.1.0',
    'description': 'Slapdash commands for interacting with AWS account',
    'long_description': 'None',
    'author': 'glyphack',
    'author_email': 'sh.hooshyari@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
