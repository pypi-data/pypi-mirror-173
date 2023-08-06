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
    'version': '0.1.1',
    'description': 'Python Epitopic Charge Calculator',
    'long_description': '# PECC (Python Epitopic Charge Calculator)\n\n### Overview\n\n\n\n### Getting started\n#### Install from PyPI (recommended)\nTo use `pecc`, run `pip install pecc` in your terminal.\n\n\n#### Usage\n\n\n#### Exit codes:\n```\n```\n\n\n#### Unit tests\n```\n```\n\n\n\n### About the source code\n- Follows [PEP8](https://peps.python.org/pep-0008/) Style Guidelines.\n- All variables are correctly type-hinted, reviewed with [static type checker](https://mypy.readthedocs.io/en/stable/)\n`mypy`.\n\n\n\n### Useful links:\n- [Corresponding GitHub repository](https://github.com/MICS-Lab/pecc)\n- [Corresponding PyPI page]()\n\n\n\n### Citation\nIf you use this software, please cite it as below.\n\n- APA:\n\n\n\n- BibTeX:\n\n\n\n### References\n',
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
