# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decode']

package_data = \
{'': ['*'], 'decode': ['data/*']}

install_requires = \
['matplotlib>=3.2,<4.0',
 'morecopy>=0.2,<0.3',
 'netcdf4>=1.5,<2.0',
 'numpy>=1.21,<2.0',
 'scikit-learn>=1.0,<2.0',
 'scipy>=1.7,<2.0',
 'tomli>=2.0,<3.0',
 'tqdm>=4.64,<5.0',
 'typing-extensions>=3.10,<4.0',
 'xarray-dataclasses>=1.2,<2.0',
 'xarray>=0.20,<0.21']

extras_require = \
{':python_full_version >= "3.7.1" and python_version < "3.8"': ['astropy>=4.3,<5.0'],
 ':python_version >= "3.8" and python_version < "3.10"': ['astropy>=5.1,<6.0']}

setup_kwargs = {
    'name': 'decode',
    'version': '0.7.1',
    'description': 'DESHIMA code for data analysis',
    'long_description': '# De:code\n\n[![Release](https://img.shields.io/pypi/v/decode?label=Release&color=cornflowerblue&style=flat-square)](https://pypi.org/pypi/decode/)\n[![Python](https://img.shields.io/pypi/pyversions/decode?label=Python&color=cornflowerblue&style=flat-square)](https://pypi.org/pypi/decode/)\n[![Downloads](https://img.shields.io/pypi/dm/decode?label=Downloads&color=cornflowerblue&style=flat-square)](https://pepy.tech/project/decode)\n[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.3384216-cornflowerblue?style=flat-square)](https://doi.org/10.5281/zenodo.3384216)\n[![Tests](https://img.shields.io/github/workflow/status/deshima-dev/decode/Tests?label=Tests&style=flat-square)](https://github.com/deshima-dev/decode/actions/tests.yml)\n\nDESHIMA code for data analysis\n\n## Installation\n\n```shell\n$ pip install decode\n```\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/deshima-dev/decode/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
