# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiopurpleair']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.0', 'pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'aiopurpleair',
    'version': '2022.10.0',
    'description': 'A Python 3, asyncio-based library to interact with the PurpleAir API',
    'long_description': '# 🚰 aiopurpleair: DESCRIPTION\n\n[![CI](https://github.com/bachya/aiopurpleair/workflows/CI/badge.svg)](https://github.com/bachya/aiopurpleair/actions)\n[![PyPi](https://img.shields.io/pypi/v/aiopurpleair.svg)](https://pypi.python.org/pypi/aiopurpleair)\n[![Version](https://img.shields.io/pypi/pyversions/aiopurpleair.svg)](https://pypi.python.org/pypi/aiopurpleair)\n[![License](https://img.shields.io/pypi/l/aiopurpleair.svg)](https://github.com/bachya/aiopurpleair/blob/main/LICENSE)\n[![Code Coverage](https://codecov.io/gh/bachya/aiopurpleair/branch/dev/graph/badge.svg)](https://codecov.io/gh/bachya/aiopurpleair)\n[![Maintainability](https://api.codeclimate.com/v1/badges/40e0f45570a0eb9aab24/maintainability)](https://codeclimate.com/github/bachya/aiopurpleair/maintainability)\n[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)\n\n<a href="https://www.buymeacoffee.com/bachya1208P" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>\n\n`aiopurpleair` is a Python 3, asyncio-based library to interact with the\n[PurpleAir](https://www2.purpleair.com/) API.\n\n- [Installation](#installation)\n- [Python Versions](#python-versions)\n- [Usage](#usage)\n- [Contributing](#contributing)\n\n# Installation\n\n```bash\npip install aiopurpleair\n```\n\n# Python Versions\n\n`aiopurpleair` is currently supported on:\n\n- Python 3.9\n- Python 3.10\n- Python 3.11\n\n# Usage\n\n# Contributing\n\n1. [Check for open features/bugs](https://github.com/bachya/aiopurpleair/issues)\n   or [initiate a discussion on one](https://github.com/bachya/aiopurpleair/issues/new).\n2. [Fork the repository](https://github.com/bachya/aiopurpleair/fork).\n3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`\n4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`\n5. Install the dev environment: `script/setup`\n6. Code your new feature or bug fix.\n7. Write tests that cover your new functionality.\n8. Run tests and ensure 100% code coverage: `nox -rs coverage`\n9. Update `README.md` with any new documentation.\n10. Add yourself to `AUTHORS.md`.\n11. Submit a pull request!\n',
    'author': 'Aaron Bach',
    'author_email': 'bachya1208@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bachya/aiopurpleair',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
