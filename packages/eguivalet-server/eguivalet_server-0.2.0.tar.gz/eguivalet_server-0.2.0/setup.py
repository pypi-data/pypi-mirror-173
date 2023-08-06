# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eguivalet_server',
 'eguivalet_server.routes',
 'eguivalet_server.routes.api',
 'eguivalet_server.routes.api.v1']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy-Utils>=0.38.2,<0.39.0',
 'SQLAlchemy>=1.4.42,<2.0.0',
 'fastapi[all]>=0.85.1,<0.86.0',
 'python-multipart>=0.0.5,<0.0.6',
 'requests>=2.28.1,<3.0.0',
 'tomli>=2.0.1,<3.0.0',
 'uvicorn>=0.18.3,<0.19.0']

setup_kwargs = {
    'name': 'eguivalet-server',
    'version': '0.2.0',
    'description': 'A server implementation for the EguiValet messaging service.',
    'long_description': '# 5G00EV25-3001 Server\n\nA server implementation for the EguiValet messaging service.\n\n|              |   |\n|--------------|---|\n| Tests (main) | [![codecov](https://codecov.io/gh/Diapolo10/5G00EV25-3001_server/branch/main/graph/badge.svg?token=zBlgCd32Aq)](https://codecov.io/gh/Diapolo10/5G00EV25-3001_server) ![Unit tests](https://github.com/diapolo10/5G00EV25-3001_server/workflows/Unit%20tests/badge.svg) ![Pylint](https://github.com/diapolo10/5G00EV25-3001_server/workflows/Pylint/badge.svg) ![Flake8](https://github.com/diapolo10/5G00EV25-3001_server/workflows/Flake8/badge.svg) |\n| Activity     | ![GitHub contributors](https://img.shields.io/github/contributors/diapolo10/5G00EV25-3001_server) ![Last commit](https://img.shields.io/github/last-commit/diapolo10/5G00EV25-3001_server?logo=github) ![GitHub all releases](https://img.shields.io/github/downloads/diapolo10/5G00EV25-3001_server/total?logo=github) ![GitHub issues](https://img.shields.io/github/issues/diapolo10/5G00EV25-3001_server) ![GitHub closed issues](https://img.shields.io/github/issues-closed/diapolo10/5G00EV25-3001_server) ![GitHub pull requests](https://img.shields.io/github/issues-pr/diapolo10/5G00EV25-3001_server) ![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/diapolo10/5G00EV25-3001_server) |\n| QA           | [![CodeFactor](https://www.codefactor.io/repository/github/diapolo10/5G00EV25-3001_server/badge?logo=codefactor)](https://www.codefactor.io/repository/github/diapolo10/5G00EV25-3001_server) |\n| Other        | [![License](https://img.shields.io/github/license/diapolo10/5G00EV25-3001_server)](https://opensource.org/licenses/MIT) [![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FDiapolo10%2F5G00EV25-3001_server.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FDiapolo10%2F5G00EV25-3001_server?ref=badge_shield) [![Requirements Status](https://requires.io/github/Diapolo10/5G00EV25-3001_server/requirements.svg?branch=main)](https://requires.io/github/Diapolo10/5G00EV25-3001_server/requirements/?branch=main) ![Repository size](https://img.shields.io/github/repo-size/diapolo10/5G00EV25-3001_server?logo=github) ![Code size](https://img.shields.io/github/languages/code-size/diapolo10/5G00EV25-3001_server?logo=github) ![Lines of code](https://img.shields.io/tokei/lines/github/diapolo10/5G00EV25-3001_server?logo=github) |\n\n## Installation\n\nThe package is currently not available on PyPI.\n\nTo run the project, download the repository. You will need to have Python 3.8\nor newer installed, as well as Poetry.\n\n```sh\npip install poetry\n```\n\nUnzip the project files, and navigate to the project directory. Run the commands\n\n```sh\npoetry shell\npoetry install\n```\n\nin order to create a virtual environment for the project and install its\ndependencies.\n\nYou can then run the project by running `eguivalet_server/main.py` while within the\nvirtual environment.\n\n<!-- markdownlint-configure-file {\n    "MD013": false\n} -->\n<!--\n    MD013: Line length\n-->\n',
    'author': 'Lari Liuhamo',
    'author_email': 'lari.liuhamo+pypi@gmail.com',
    'maintainer': 'Juha Järvinen',
    'maintainer_email': 'juha.3.jarvinen@tuni.fi',
    'url': 'https://pypi.org/project/5G00EV25-3001_server/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
