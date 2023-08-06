# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mediathequeroubaix', 'mediathequeroubaix.fetch_loans']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'mediathequeroubaix',
    'version': '0.2.0',
    'description': 'Client for the library of Roubaix (Médiathèque Roubaix)',
    'long_description': '<p align="center" width="100%">\n  <img src="doc/banner.png" alt="MediathequeRoubaix.py"/>\n</p>\n\n# Python CLI for the library of Roubaix (Médiathèque Roubaix)\n\n[![PyPI](https://img.shields.io/pypi/v/mediathequeroubaix?style=flat-square)](https://pypi.python.org/pypi/mediathequeroubaix/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mediathequeroubaix?style=flat-square)](https://pypi.python.org/pypi/mediathequeroubaix/)\n[![PyPI - License](https://img.shields.io/pypi/l/mediathequeroubaix?style=flat-square)](https://pypi.python.org/pypi/mediathequeroubaix/)\n\n---\n\n**Source Code**: [https://github.com/tomsquest/mediathequeroubaix.py](https://github.com/tomsquest/mediathequeroubaix.py)\n\n**PyPI**: [https://pypi.org/project/mediathequeroubaix/](https://pypi.org/project/mediathequeroubaix/)\n\n---\n\n<!-- START doctoc generated TOC please keep comment here to allow auto update -->\n<!-- DON\'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->\n## Table of Contents\n\n- [Features](#features)\n  - [Loans](#loans)\n  - [Usage](#usage)\n- [Why I am doing this](#why-i-am-doing-this)\n- [Changelog](#changelog)\n- [Installation](#installation)\n- [Development](#development)\n  - [Testing](#testing)\n  - [Pre-commit](#pre-commit)\n  - [Releasing](#releasing)\n- [Credits](#credits)\n\n<!-- END doctoc generated TOC please keep comment here to allow auto update -->\n\n## Features\n\nMédiathèqueRoubaix.py is a client for the **libray of Roubaix**, [mediathequederoubaix.fr](http://www.mediathequederoubaix.fr/).  \n\n<p align="center" width="100%">\n  <img src="doc/mr_homepage.png" alt="Screenshot mediathequederoubaix.fr"/>\n</p>\n\n### Loans\n\n1. Display a **list of your loans**\n2. ...for **many card holders** at once (family) (TODO)\n3. Quickly get the **next return date** for all you cards (TODO)\n\n### Usage\n\nVery basically for now, to list the loans of a single user defined in environment variable\n\n```shell\n$ export USERNAME="X001002003"\n$ export PASSWORD="password00"\n\n$ python src/mediathequeroubaix/main.py\nGetting loans of user: X001002003\n\nNumber of loans: 2\n- [ 1/02] Machine learning avec Scikit-learn, due on: 2022-12-04, NOT renewable\n- [ 2/02] Programmation Python avancée, due on: 2022-12-04, renewable\n```\n\n## Why I am doing this\n\nI created this project to:\n1. Learn Functional Programing\n2. Learn typed and modern Python\n3. Be able to quickly list and renew my loans\n\n## Changelog\n\nSee [CHANGELOG.md](CHANGELOG.md)\n\n## Installation\n\n```sh\npip install mediathequeroubaix\n```\n\n## Development\n\n* Clone this repository\n* Requirements:\n  * [Poetry](https://python-poetry.org/)\n  * Python 3.10\n* Create a virtual environment and install the dependencies\n\n```sh\npoetry install\n```\n\n* Activate the virtual environment\n\n```sh\npoetry shell\n```\n\n### Testing\n\n```sh\npytest\n```\n\n### Pre-commit\n\n```sh\npre-commit install\n```\n\nOr if you want to run all checks for all files:\n\n```sh\npre-commit run --all-files\n```\n\n### Releasing\n\nTrigger the [Draft release workflow](https://github.com/tomsquest/mediathequeroubaix.py/actions/workflows/draft_release.yml)\n(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.\n\nFind the draft release from the\n[GitHub releases](https://github.com/tomsquest/mediathequeroubaix.py/releases) and publish it. When\n a release is published, it\'ll trigger [release](https://github.com/tomsquest/mediathequeroubaix.py/blob/master/.github/workflows/release.yml) workflow which creates PyPI\n release.\n\n\n## Credits\n\n- Background and color from [PrettySnap](https://prettysnap.app/)\n- Python project bootstrapped using [Wolt template](https://github.com/woltapp/wolt-python-package-cookiecutter)\n',
    'author': 'Thomas Queste',
    'author_email': 'tom@tomsquest.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://tomsquest.github.io/mediathequeroubaix.py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<3.11.0',
}


setup(**setup_kwargs)
