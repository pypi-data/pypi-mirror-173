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
    'version': '1.0.3',
    'description': 'Copy fields from pyproject.toml to source directory',
    'long_description': '# poetry-plugin-pycopy\n\n<!--- These are examples. See https://shields.io for others or to customize this set of shields. You might want to include dependencies, project status and licence info here --->\n![GitHub repo size](https://img.shields.io/github/repo-size/danielfajt/poetry-plugin-pycopy)\n![GitHub contributors](https://img.shields.io/github/contributors/danielfajt/poetry-plugin-pycopy)\n![GitHub stars](https://img.shields.io/github/stars/danielfajt/poetry-plugin-pycopy?style=social)\n![GitHub forks](https://img.shields.io/github/forks/danielfajt/poetry-plugin-pycopy?style=social)\n![Twitter Follow](https://img.shields.io/twitter/follow/danielfajt?style=social)\n\nThis plugin adds command `pycopy` to Poetry which will copy information from `pyproject.toml` to `source` directory. \n\nThe goal is to have `pyproject.toml` as a single source of truth for app version, name, description etc. and to have these values available during a program runtime.\n\n## Use case\nFastAPI app in which you want to show application name or version in API docs.\n\n\n## Installation\n\nFrom Pypi:\n```\n$ poetry self add poetry-plugin-pycopy\n```\n\n## Usage\n\n```\n$ poetry pycopy\n```\n\n## Plugin configuration in `pyproject.toml`\n\n```\n[tool.poetry-plugin-pycopy]\nkeys = ["name", "version", "description"]\ndest_dir = "<some_package_name>"\ndest_file = "__init__.py"\n```\n- `keys` list tells which fields should by copied from `[tool.poetry]`\n- `dest_dir` is package/module root\n- `dest_file` is the name of an output file\n\nPlugin also runs with `$poetry version` command automatically. So when you use version bump, e.g.: `$poetry version patch` the plugin will copy the new version value into the output file.\n\n## Output file example\nThe `dest_file` is set to `__init__.py`. Thus the plugin will create or replace that file with current values for a given `keys`. For example:\n\n```\n__name = "poetry-plugin-pycopy"\n__version = "1.0.0"\n__description = "Copy fields from pyproject.toml to source directory"\n\n```\n\n-> https://unlicense.org/',
    'author': 'Daniel Fajt',
    'author_email': 'daniel29se@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
