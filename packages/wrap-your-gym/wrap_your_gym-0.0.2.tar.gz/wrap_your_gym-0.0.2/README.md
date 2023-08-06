# Wrap Your Gym!

![PyPI](https://img.shields.io/pypi/v/wrap-your-gym?style=flat-square)
![GitHub Workflow Status (master)](https://img.shields.io/github/workflow/status/sebimarkgraf/wrap-your-gym/Test%20&%20Lint/master?style=flat-square)
![Coveralls github branch](https://img.shields.io/coveralls/github/sebimarkgraf/wrap-your-gym/master?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wrap-your-gym?style=flat-square)
![PyPI - License](https://img.shields.io/pypi/l/wrap-your-gym?style=flat-square)

Common OpenAI gym wrappers found during my journeys.
This repository collects a multitude of wrappers that I needed for my own implementation
or extracted from other research repositories.

Why create this repository?
As most research implementations opt for changing environment implementations instead of wrappers, it gets very complicated
to replace the originally used environment. 
This repository extracts all modifications to the environment and makes it possible to just plug and play
a custom environment with a multitude of wrappers.
I hope, that this convinces other researchers of the benefit of wrappers and changes the way we implement environments in
the long run.

## OpenAI Gym Compatibility
This package uses the new Gym API where it is necessary to use one specific API.
While most wrappers should be usable with the old API, an easy fix is the usage of the 
StepAPICompability wrapper implemented in Gym.
E.g.
```python
from gym.wrappers import StepAPICompability
from wrap_your_gym import ResetObs

env = ... # Your Env
env = StepAPICompability(env, truncated_bool=True)
env = ResetObs(env) # or another wrapper
env = StepAPICompability(env, truncated_bool=False) # depending on the API your code was implemented for
```


## Requirements

* Python 3.7.0 or newer
* Gym (obviously)
* Numpy
* For the torch module: PyTorch

## Installation

```sh
pip install wrap-your-gym
```

## Development

This project uses [poetry](https://poetry.eustace.io/) for packaging and
managing all dependencies and [pre-commit](https://pre-commit.com/) to run
[flake8](http://flake8.pycqa.org/), [isort](https://pycqa.github.io/isort/),
[mypy](http://mypy-lang.org/) and [black](https://github.com/python/black).

Additionally, [pdbpp](https://github.com/pdbpp/pdbpp) and [better-exceptions](https://github.com/qix-/better-exceptions) 
are installed to provide a better debugging experience.
To enable `better-exceptions` you have to run `export BETTER_EXCEPTIONS=1` in your current session/terminal.

Clone this repository and run

```bash
poetry install
poetry run pre-commit install
```

to create a virtual environment containing all dependencies.
Afterwards, You can run the test suite using

```bash
poetry run pytest
```

This repository follows the [Conventional Commits](https://www.conventionalcommits.org/)
style.
