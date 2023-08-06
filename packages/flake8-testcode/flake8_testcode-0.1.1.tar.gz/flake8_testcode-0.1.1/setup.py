# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_testcode']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.8.4,<6']

entry_points = \
{'flake8.extension': ['TMA = flake8_testcode:Plugin']}

setup_kwargs = {
    'name': 'flake8-testcode',
    'version': '0.1.1',
    'description': 'Plugin to catch bad style specific to testcode.',
    'long_description': '![testing](https://github.com/ewald91/flake8-testcode/actions/workflows/build.yml/badge.svg)\n[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)\n[![Active](http://img.shields.io/badge/Status-Active-green.svg)](https://tterb.github.io) \n<!-- [![PyPi Version](https://img.shields.io/pypi/v/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/) -->\n<!-- [![Coveralls](https://img.shields.io/coveralls/jekyll/jekyll.svg?style=flat)]() -->\n\n## flake8 codes\n\n| Code   | Description                          |\n|--------|--------------------------------------|\n| TMA001 | Missing assertion in test definition |\n\n\n## Poetry\n\nenter virtual environment  (first time) \n`poetry shell`\n\nre-enter virtual environment:\n`& ((poetry env info --path) + "\\Scripts\\activate.ps1")`',
    'author': 'Ewald Verhoeven',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Ewald91/flake8-testcode',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
