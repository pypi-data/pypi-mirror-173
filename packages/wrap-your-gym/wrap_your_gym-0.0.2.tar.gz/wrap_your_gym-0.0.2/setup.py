# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wrap_your_gym']

package_data = \
{'': ['*']}

install_requires = \
['gym>0.20.0']

setup_kwargs = {
    'name': 'wrap-your-gym',
    'version': '0.0.2',
    'description': 'Common OpenAI Gym Wrappers',
    'long_description': '# Wrap Your Gym!\n\n![PyPI](https://img.shields.io/pypi/v/wrap-your-gym?style=flat-square)\n![GitHub Workflow Status (master)](https://img.shields.io/github/workflow/status/sebimarkgraf/wrap-your-gym/Test%20&%20Lint/master?style=flat-square)\n![Coveralls github branch](https://img.shields.io/coveralls/github/sebimarkgraf/wrap-your-gym/master?style=flat-square)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wrap-your-gym?style=flat-square)\n![PyPI - License](https://img.shields.io/pypi/l/wrap-your-gym?style=flat-square)\n\nCommon OpenAI gym wrappers found during my journeys.\nThis repository collects a multitude of wrappers that I needed for my own implementation\nor extracted from other research repositories.\n\nWhy create this repository?\nAs most research implementations opt for changing environment implementations instead of wrappers, it gets very complicated\nto replace the originally used environment. \nThis repository extracts all modifications to the environment and makes it possible to just plug and play\na custom environment with a multitude of wrappers.\nI hope, that this convinces other researchers of the benefit of wrappers and changes the way we implement environments in\nthe long run.\n\n## OpenAI Gym Compatibility\nThis package uses the new Gym API where it is necessary to use one specific API.\nWhile most wrappers should be usable with the old API, an easy fix is the usage of the \nStepAPICompability wrapper implemented in Gym.\nE.g.\n```python\nfrom gym.wrappers import StepAPICompability\nfrom wrap_your_gym import ResetObs\n\nenv = ... # Your Env\nenv = StepAPICompability(env, truncated_bool=True)\nenv = ResetObs(env) # or another wrapper\nenv = StepAPICompability(env, truncated_bool=False) # depending on the API your code was implemented for\n```\n\n\n## Requirements\n\n* Python 3.7.0 or newer\n* Gym (obviously)\n* Numpy\n* For the torch module: PyTorch\n\n## Installation\n\n```sh\npip install wrap-your-gym\n```\n\n## Development\n\nThis project uses [poetry](https://poetry.eustace.io/) for packaging and\nmanaging all dependencies and [pre-commit](https://pre-commit.com/) to run\n[flake8](http://flake8.pycqa.org/), [isort](https://pycqa.github.io/isort/),\n[mypy](http://mypy-lang.org/) and [black](https://github.com/python/black).\n\nAdditionally, [pdbpp](https://github.com/pdbpp/pdbpp) and [better-exceptions](https://github.com/qix-/better-exceptions) \nare installed to provide a better debugging experience.\nTo enable `better-exceptions` you have to run `export BETTER_EXCEPTIONS=1` in your current session/terminal.\n\nClone this repository and run\n\n```bash\npoetry install\npoetry run pre-commit install\n```\n\nto create a virtual environment containing all dependencies.\nAfterwards, You can run the test suite using\n\n```bash\npoetry run pytest\n```\n\nThis repository follows the [Conventional Commits](https://www.conventionalcommits.org/)\nstyle.\n',
    'author': 'Sebastian Markgraf',
    'author_email': 'sebastian-markgraf@t-online.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sebimarkgraf/wrap-your-gym',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0',
}


setup(**setup_kwargs)
