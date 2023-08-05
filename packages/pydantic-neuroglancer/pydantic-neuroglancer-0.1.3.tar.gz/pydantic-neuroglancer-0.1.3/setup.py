# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydantic_neuroglancer']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'pydantic-neuroglancer',
    'version': '0.1.3',
    'description': 'Pydantic models for neuroglancer viewer state',
    'long_description': None,
    'author': 'Davis Vann Bennett',
    'author_email': 'davis.v.bennett@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4',
}


setup(**setup_kwargs)
