# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['punsctl']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['punsctl = punsctl.main:main']}

setup_kwargs = {
    'name': 'punsctl',
    'version': '0.1.0',
    'description': "POSIX User's Namespace Control",
    'long_description': '### `The project is currently under development and is not ready for use in production.`\n\n# punsctl - POSIX User\'s Namespace Control\n\n[![codecov](https://codecov.io/github/alekbuza/punsctl/branch/main/graph/badge.svg?token=OMHOSME5ZB)](https://codecov.io/github/alekbuza/punsctl)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/punsctl)\n![PyPI - Implementation](https://img.shields.io/pypi/implementation/punsctl)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/punsctl)\n\nThe `punsctl` utility manages multiple namespaces (user environments) for the current POSIX user.\nThat means the user can have multiple "_profiles_" for the same or different tool configurations in the same user account\n(`~/.ssh`, `~/.gitconfig`, `~/.gnupg`, `~/.config`, `~/.config/nvim`, ...).\nThe user can create, delete, activate and deactivate namespaces without additional permissions.\n\n## Installation\n\n```sh\npip install punsctl\n```\n\n## Usage\n\n### Create a new namespace\n```sh\npunsctl -c <namespace>\n```\n\n### List all namespaces\n```sh\npunsctl -l\n```\n\n### Activate a namespace\n```sh\npunsctl -a <namespace>\n```\n\n### Deactivate namespaces\n```sh\npunsctl -d\n```\n\n### List all namespaces for the non-default root path (`~/.ns`)\n```sh\npunsctl -p <root_path> -l\n```\n',
    'author': 'Aleksandar Buza',
    'author_email': 'me@aleksandarbuza.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alekbuza/punsctl',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
