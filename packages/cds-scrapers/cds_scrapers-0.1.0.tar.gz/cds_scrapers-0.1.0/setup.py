# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cds_scrapers']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.1,<2.0.0',
 'pytest>=7.1.3,<8.0.0',
 'requests>=2.28.1,<3.0.0',
 'textstat>=0.7.3,<0.8.0']

setup_kwargs = {
    'name': 'cds-scrapers',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'albertomerango',
    'author_email': 'alberto.marengo@coeuraj.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
