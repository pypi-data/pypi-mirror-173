# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloudops', 'cloudops.google']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-bigquery>=3.1.0,<4.0.0',
 'pandas-gbq>=0.17.5,<0.18.0',
 'pandas>=1.4.2,<2.0.0',
 'pydantic>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'cloudops-google-bigquery',
    'version': '0.1.4',
    'description': 'The cloudops-google-bigquery package',
    'long_description': '# cloudops-google-bigquery\n',
    'author': 'Manuel Castillo',
    'author_email': 'manucalop@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/manucalop/cloudops-google-bigquery',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
