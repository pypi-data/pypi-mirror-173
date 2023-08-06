# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utilz', 'utilz.tests']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.1.0,<2.0.0',
 'matplotlib>=3.1.0,<4.0.0',
 'numpy>=1.16,<2.0',
 'pandas>=1.2.0,<2.0.0',
 'seaborn>=0.12.0',
 'toolz>=0.12.0,<0.13.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'py-utilz',
    'version': '0.3.2',
    'description': 'Faster, easier, more robust python data analysis',
    'long_description': "# Utilz\n![Build Status](https://github.com/ejolly/utilz/workflows/Utilz/badge.svg)\n[![Coverage Status](https://coveralls.io/repos/github/ejolly/utilz/badge.svg?branch=master)](https://coveralls.io/github/ejolly/utilz?branch=master)\n![Python Versions](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue)\n![Platforms](https://img.shields.io/badge/platform-linux%20%7C%20osx%20%7C%20win-blue)\n\nConvenient helper functions, decorators, and data analysis tools to make life easier with minimal dependencies:\n\n`pip install py-utilz`\n\n```python\nfrom utilz import mapcat\n\n# Combine function results into a list, array, or dataframe\nmapcat(myfunc, myiterable) \n\n# Syntactic sugar for joblib.Parallel\nmapcat(myfunc, myiterable, n_jobs=4)\n```\n\n```python\nfrom utilz import log, maybe\n\n# Print the shape of args and outputs before and after execute\n@log\ndef myfunc(args):\n    return out\n\n# Only run myfunc if results.csv doesn't eist\n@maybe('results.csv')\ndef myfunc(args):\n    return out\n```\n\n\n## Development\n\n1. Install [poetry](https://python-poetry.org/): `curl -sSL https://install.python-poetry.org | python`\n2. Setup virtual environment `poetry install`\n3. Run all tests: `poetry run pytest`\n4. Live render docs: `poetry run mkdocs serve`\n\n### Additional poetry/virtual environment commands\n- Activate environment in current shell: `source activate .venv/bin/activate`\n- Activate environment in sub-process shell: `poetry shell`\n- Add/remove additional packages: `poetry add/remove package_name`\n- Build local package: `poetry build`\n- Deploy to pypi: `poetry publish` (requires auth)\n",
    'author': 'ejolly',
    'author_email': 'eshin.jolly@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
