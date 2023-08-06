# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rvdata']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rvdata',
    'version': '0.1.0',
    'description': 'Radial Velocity Data',
    'long_description': '\n# RVdata\n\n\n<div align="center">\n\n[![PyPI - Version](https://img.shields.io/pypi/v/rvdata.svg)](https://pypi.python.org/pypi/rvdata)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rvdata.svg)](https://pypi.python.org/pypi/rvdata)\n[![Tests](https://github.com/j-faria/rvdata/workflows/tests/badge.svg)](https://github.com/j-faria/rvdata/actions?workflow=tests)\n[![Codecov](https://codecov.io/gh/j-faria/rvdata/branch/main/graph/badge.svg)](https://codecov.io/gh/j-faria/rvdata)\n[![Read the Docs](https://readthedocs.org/projects/rvdata/badge/)](https://rvdata.readthedocs.io/)\n[![PyPI - License](https://img.shields.io/pypi/l/rvdata.svg)](https://pypi.python.org/pypi/rvdata)\n\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](https://www.contributor-covenant.org/version/2/0/code_of_conduct/)\n\n</div>\n\n\nRadial Velocity Data\n\n\n* GitHub repo: <https://github.com/j-faria/rvdata.git>\n* Documentation: <https://rvdata.readthedocs.io>\n* Free software: MIT\n\n\n## Features\n\n* TODO\n\n## Quickstart\n\nTODO\n\n## Credits\n\nThis package was created with [Cookiecutter][cookiecutter] and the [fedejaure/cookiecutter-modern-pypackage][cookiecutter-modern-pypackage] project template.\n\n[cookiecutter]: https://github.com/cookiecutter/cookiecutter\n[cookiecutter-modern-pypackage]: https://github.com/fedejaure/cookiecutter-modern-pypackage\n',
    'author': 'João Faria',
    'author_email': 'joao.faria@astro.up.pt',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/j-faria/rvdata',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
