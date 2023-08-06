# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decide',
 'decide.data',
 'decide.data.tests',
 'decide.model',
 'decide.model.observers',
 'decide.model.observers.tests',
 'decide.model.test',
 'decide.qt',
 'decide.qt.inputwindow',
 'decide.qt.inputwindow.tests',
 'decide.qt.mainwindow',
 'decide.qt.mainwindow.tests',
 'decide.results',
 'decide.tests']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5==5.12.3',
 'blinker==1.5',
 'matplotlib==3.6.0',
 'numpy==1.23.4',
 'pandas==1.5.0',
 'peewee==3.14.4',
 'typesystem==0.2.2']

entry_points = \
{'console_scripts': ['decide-cli = decide.cli:main',
                     'decide-gui = decide.gui:main']}

setup_kwargs = {
    'name': 'decide-exchange-model',
    'version': '2022.1.16',
    'description': 'Decide exchange model',
    'long_description': '[![Build Status](https://travis-ci.org/foarsitter/decide-exchange-model.svg?branch=master)](https://travis-ci.org/foarsitter/decide-exchange-model)\n[![Code Climate](https://codeclimate.com/github/foarsitter/decide-exchange-model/badges/gpa.svg)](https://codeclimate.com/github/foarsitter/decide-exchange-model)\n[![Test Coverage](https://codeclimate.com/github/foarsitter/decide-exchange-model/badges/coverage.svg)](https://codeclimate.com/github/foarsitter/decide-exchange-model/coverage)\n[![PyPI](https://img.shields.io/pypi/v/decide-exchange-model.svg)](https://pypi.org/project/decide-exchange-model/)\n[![Anaconda-Server Badge](https://anaconda.org/jelmert/decide-exchange-model/badges/version.svg)](https://anaconda.org/jelmert/decide-exchange-model)\n[![Issue Count](https://codeclimate.com/github/foarsitter/decide-exchange-model/badges/issue_count.svg)](https://codeclimate.com/github/foarsitter/decide-exchange-model)\n\n# Decide Exchange Model\nEqual Gain Model implementation in the Python programming language. Read the documentation on https://foarsitter.github.io/decide-exchange-model/',
    'author': 'Jelmer Draaijer',
    'author_email': 'info@jelmert.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
