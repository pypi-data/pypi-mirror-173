# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_plugin_pycopy']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.2,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['pycopy = plugin:PoetryPluginPycopy']}

setup_kwargs = {
    'name': 'poetry-plugin-pycopy',
    'version': '1.0.0',
    'description': 'Copy fields from pyproject.toml to source directory',
    'long_description': '',
    'author': 'Daniel Fajt',
    'author_email': 'daniel29se@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
