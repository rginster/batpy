[![ci-cd](https://github.com/rginster/batpy/actions/workflows/ci-cd.yaml/badge.svg)](https://github.com/rginster/batpy/actions/workflows/ci-cd.yaml)
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

## Documentation

Documentation for `batpy` is available at [GitHub Pages](https://rginster.github.io/batpy/), including an example and documentation on all the modules and functions.

## Usage

`batpy` is able to read, write, and calculate batteries in the [BatPaC tool](https://www.anl.gov/partnerships/batpac-battery-manufacturing-cost-estimation).



```python
from batpy.batpac_battery import BatpacBattery
from batpy.batpac_tool import BatpacTool
from batpy import batpac_datasets

# Paths to TOML configurations on local system
BATPY_BATPAC_EXCEL = "./BatPaC 5.0 2022-07-22.xlsm"

BATPY_BATPAC_BATTERY_CONFIG = "./batpy_batteries_config.toml"
BATPY_BATPAC_USER_INPUT_CONFIG = (
    "./batpy_batpac_user_input_cells.toml"
)
BATPY_BATPAC_TOOL_CONFIG = "./batpy_batpac_config.toml"

BATPY_BATPAC_TOOL_CALCULATION_VALIDATION_CONFIG = (
    "./batpy_batpac_calculation_and_validation_results.toml"
)

ADDITIONAL_USER_DEFINED_RESULTS_CELLS = (
    "./batpy_batpac_summary_of_results.toml"
)

# Get included datasets
# Show available versions
batpac_datasets.get_available_batpy_dataset_versions()

# Show latest version
batpac_datasets.get_latest_batpy_dataset_version()


# Show available dataset of specified version (default latest)
batpac_datasets.get_available_batpy_dataset_names()


# Load included dataset:
batpy_batpac_battery_design = batpac_datasets.get_batpy_dataset(
    "batpy_batpac_battery_design", "0.1.0"
)


# Create batteries
bat1 = BatpacBattery("Battery 1")
bat2 = BatpacBattery("Battery 2")
bat3 = BatpacBattery("Battery 3")
bat4 = BatpacBattery("Battery 4")
bat5 = BatpacBattery("Battery 5")
bat6 = BatpacBattery("Battery 6")
bat7 = BatpacBattery("Battery 7")

# Change battery properties
# a) Write individual properties for created batteries
bat1.set_new_property("Dashboard", "Number of modules in parallel", 10)

# b) Load individiual battery configuration from file
bat2.load_battery_file(
    BATPY_BATPAC_BATTERY_CONFIG, "Battery 2"
)

# Create BatPaC instance
battery_calculation = BatpacTool(
    BATPY_BATPAC_EXCEL,
    BATPY_BATPAC_USER_INPUT_CONFIG,
    BATPY_BATPAC_TOOL_CALCULATION_VALIDATION_CONFIG,
    excel_visible=True
)

# Add batteries to BatPaC instance
# a) Add individual batteries, which were created before
battery_calculation.add_battery(
    [
        bat1,
        bat2,
        bat3,
        bat4,
        bat5,
        bat6,
        bat7,
    ]
)

# b) Create new batteries from configuration file (will overwrite all batteries)
battery_calculation.load_batteries_file(
    BATPY_BATPAC_BATTERY_CONFIG,
    [
        bat1,
        bat2,
        bat3,
        bat4,
        bat5,
        bat6,
        bat7,
    ],
)

# Load configuration file for BatPaC instance
battery_calculation.load_batpac_file(BATPY_BATPAC_TOOL_CONFIG)

# Write configuration in Excel file and calculate batteries
battery_calculation.calculate()
battery_calculation.read_calculation_and_validation_results()

# Read additional user defined cells
# a) From file path
user_results = battery_calculation.read_from_user_input(
    ADDITIONAL_USER_DEFINED_RESULTS_CELLS
)
print(user_results)
print(user_results["Summary of Results"]["Battery 1"])

# b) From included configuration
user_results_included_configuration = battery_calculation.read_from_user_input(
    batpy_batpac_battery_design
)
print(user_results_included_configuration)
print(user_results_included_configuration["Battery Design"]["Battery 1"])

# Save configuration from Excel:
battery_calculation.save_config(
    batpac_path="./saved_batpac_config.toml",
    battery_path="./saved_batteries_config.toml",
)

# Save Excel file
battery_calculation.save("./saved_BatPaC.xlsm")

# Close Excel file
battery_calculation.close()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`batpy` was created by [Raphael Ginster](https://www.tu-braunschweig.de/en/aip/pl/team/ginster). It is licensed under the terms of the MIT license.

## Credits

`batpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
