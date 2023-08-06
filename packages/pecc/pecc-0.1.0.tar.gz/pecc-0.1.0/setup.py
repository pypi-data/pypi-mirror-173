# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pecc']

package_data = \
{'': ['*'], 'pecc': ['data/*']}

install_requires = \
['openpyxl>=3.0.10,<4.0.0', 'pandas>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'pecc',
    'version': '0.1.0',
    'description': 'Python Epitopic Charge Calculator',
    'long_description': 'None',
    'author': 'JasonMendoza2008',
    'author_email': 'lhotteromain@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
