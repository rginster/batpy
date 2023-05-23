![BatPy](https://raw.githubusercontent.com/rginster/batpy/main/BatPy.svg)
[![ci](https://github.com/rginster/batpy/actions/workflows/ci.yaml/badge.svg)](https://github.com/rginster/batpy/actions/workflows/ci.yaml)
[![cd](https://github.com/rginster/batpy/actions/workflows/ci-cd.yaml/badge.svg)](https://github.com/rginster/batpy/actions/workflows/ci-cd.yaml)
[![Docs](https://github.com/rginster/batpy/actions/workflows/documentation.yaml/badge.svg)](https://github.com/rginster/batpy/actions/workflows/documentation.yaml)
[![pages-build-deployment](https://github.com/rginster/batpy/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/rginster/batpy/actions/workflows/pages/pages-build-deployment)
[![codecov](https://codecov.io/gh/rginster/batpy/branch/main/graph/badge.svg?token=JH8L3B14AW)](https://codecov.io/gh/rginster/batpy)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/batpy)
[![PyPi](https://img.shields.io/pypi/v/batpy.svg)](https://pypi.python.org/pypi/batpy)
[![PyPi](https://img.shields.io/pypi/dm/batpy.svg)](https://pypi.python.org/pypi/batpy)

# batpy

`batpy` is a Python wrapper for [Argonne National Laboratory's](https://www.anl.gov) Microsoft Excel-based [software modeling tool BatPaC](https://www.anl.gov/partnerships/batpac-battery-manufacturing-cost-estimation).

## Installation

`batpy` is available from [PyPI](https://pypi.org/project/batpy/), and currently requires Python 3.10 or newer. It can be installed with:
```bash
$ pip install batpy
```

## Usage and documentation

`batpy` is able to read, write, and calculate batteries in the [BatPaC tool](https://www.anl.gov/partnerships/batpac-battery-manufacturing-cost-estimation). Furthermore, `batpy` can export the calculated batteries to a [`brightway2`](https://pypi.org/project/brightway2/) Excel workbook, which can be imported directly into [`brightway2`](https://pypi.org/project/brightway2/).

Documentation for `batpy` is available at [GitHub Pages](https://rginster.github.io/batpy/), including an example and documentation on all the modules and functions.

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`batpy` was created by [Raphael Ginster](https://www.tu-braunschweig.de/en/aip/pl/team/ginster). It is licensed under the terms of the MIT license.

## Credits

`batpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
