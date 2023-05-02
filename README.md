# batpy

`batpy` is a Python wrapper for [Argonne National Laboratory's](https://www.anl.gov) Microsoft Excel-based [software modeling tool BatPaC](https://www.anl.gov/partnerships/batpac-battery-manufacturing-cost-estimation).

## Installation

```bash
$ pip install batpy
```

## Usage

`batpy` is able to read, write, and calculate batteries in the [BatPaC tool](https://www.anl.gov/partnerships/batpac-battery-manufacturing-cost-estimation).



```python
from batpy.BatPaC_battery import BatPaC_battery
from batpy.BatPaC_tool import BatPaC_tool

# Create batteries
bat1 = BatPaC_battery("Battery 1")
bat2 = BatPaC_battery("Battery 2")
bat3 = BatPaC_battery("Battery 3")
bat4 = BatPaC_battery("Battery 4")
bat5 = BatPaC_battery("Battery 5")
bat6 = BatPaC_battery("Battery 6")
bat7 = BatPaC_battery("Battery 7")

# Change battery properties
# a) Write individual properties for created batteries
bat1.set_new_property("Dashboard", "Number of modules in parallel", 100)

# b) Load individiual battery configuration from file
bat2.load_battery_file(
    "./battery_config.toml", "Battery"
)

# Create BatPaC instance
battery_calculation = BatPaC_tool(
    "./BatPaC 5.0 2022-07-22.xlsm",
    "./BatPaC_user_input_cells.toml",
    "./BatPaC_calculation_and_validation_results.toml",
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
    "./batteries_config.toml",
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
battery_calculation.load_batpac_file("./BatPaC_config.toml")

# Write configuration in Excel file and calculate batteries
battery_calculation.calculate()
battery_calculation.read_calculation_and_validation_results()

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
