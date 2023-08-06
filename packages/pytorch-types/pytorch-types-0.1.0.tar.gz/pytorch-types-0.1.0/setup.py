# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytorch_types']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.4,<2.0.0', 'pydantic>=1.0.0,<2.0.0', 'torch>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'pytorch-types',
    'version': '0.1.0',
    'description': 'Pytorch project template and related tools',
    'long_description': '=============\nPytorch Types\n=============\n\n.. image:: https://badge.fury.io/py/pytorch-types.svg\n       :target: https://badge.fury.io/py/pytorch-types\n\n.. image:: https://img.shields.io/pypi/pyversions/pytorch-types.svg\n       :target: https://pypi.python.org/pypi/pytorch-types\n\n.. image:: https://readthedocs.org/projects/pytorch-types/badge/?version=latest\n       :target: https://pytorch-types.readthedocs.io/en/latest/?badge=latest\n\n.. image:: https://img.shields.io/pypi/l/pytorch-types.svg\n       :target: https://pypi.python.org/pypi/pytorch-types\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n\nPytorch typing for pydantic.\n\nInstall from pypi using pip or poetry:\n\n.. code-block::\n\n    poetry add pytorch-types\n    # pip install pytorch-types\n',
    'author': 'NextML AB',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nextml-code/pytorch-types',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
