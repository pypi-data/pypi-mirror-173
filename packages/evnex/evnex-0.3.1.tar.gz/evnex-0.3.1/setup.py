# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['evnex', 'evnex.schema', 'evnex.schema.v3']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0',
 'pycognito==2022.8.0',
 'pydantic>=1.10,<2.0',
 'tenacity>=8.1,<9.0']

setup_kwargs = {
    'name': 'evnex',
    'version': '0.3.1',
    'description': 'A Python wrapper for the EVNEX Cloud API',
    'long_description': None,
    'author': 'Brian Thorne',
    'author_email': 'brian@hardbyte.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
