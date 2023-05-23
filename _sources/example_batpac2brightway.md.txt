# Example usage of BatPy's brightway2 export
`batpy` is able to export a calculated battery from BatPaC as a Life Cycle Inventory Excel file, which can be imported in brightway2. In order to use `batpy`in a project for brightway2 export, follow the example below.

## Import


```python
# included datasets
from batpy import datasets

# batpac battery and tool classes
from batpy.batpac_battery import BatpacBattery
from batpy.batpac_tool import BatpacTool

# brightway2 class
from batpy.brightway import BrightwayConnector

# utility function for combining multiple configuration files
from batpy.utility_functions import combine_configuration

# pathlib for filesystem path handling
from pathlib import Path

```

## Paths to Excel files and to TOML configuration


```python
# Get BatPaC: https://www.anl.gov/partnerships/batpac-battery-manufacturing-cost-estimation
BATPY_BATPAC_EXCEL = Path("./example_data/excel_workbooks/dummy_BatPaC.xlsx")

# Brightway workbook is included
BRIGHTWAY2_EXCEL = Path("./example_data/excel_workbooks/BatPaC-Brightway.xlsx")

# brightway2 configuration
BRIGHTWAY_CONFIG = Path(
    "./example_data/conf_brightway/batpy_batpac2brightway.toml"
)
```

## Get included datasets

Show available dataset of specified version (default latest):


```python
datasets.get_available_batpy_dataset_versions()
```




    [Version('0.3.0'), Version('0.0.0'), Version('0.1.0')]




```python
datasets.get_available_batpy_datasets()
```




    {'batpy_batteries_config.toml': 'Example configuration for batteries',
     'batpy_batpac_config.toml': 'Example configuration for BatPaC tool',
     'batpy_batpac_summary_of_results.toml': 'Configuration for worksheet Summary of Results in BatPaC Excel',
     'batpy_batpac_calculation_and_validation_results.toml': 'Configuration for calculation and validation results in BatPaC Excel',
     'batpy_batpac_user_input_cells.toml': 'Configuration for standard user input cells in BatPaC Excel',
     'batpy_batpac_battery_design.toml': 'Configuration for worksheet battery design in BatPaC Excel',
     'batpy_batpac2brightway.toml': 'Configuration for brightway2 export'}



Export integrated dataset


```python
datasets.copy_integrated_dataset("batpy_batpac2brightway", BRIGHTWAY_CONFIG)

```

Load multiple included datasets for BatPaC configuration and combine them:


```python
batpy_batpac_dataset = combine_configuration(
    [
        datasets.get_batpy_dataset("batpy_batpac_battery_design"),
        datasets.get_batpy_dataset("batpy_batpac_summary_of_results"),
    ]
)
```

Save integrated brightway2 Excel file


```python
datasets.copy_integrated_brightway_workbook(BRIGHTWAY2_EXCEL)
```

## Batteries
### Create batteries


```python
bat1 = BatpacBattery("Battery 1")
bat2 = BatpacBattery("Battery 2")
bat3 = BatpacBattery("Battery 3")
bat4 = BatpacBattery("Battery 4")
bat5 = BatpacBattery("Battery 5")
bat6 = BatpacBattery("Battery 6")
bat7 = BatpacBattery("Battery 7")

```

## BatPaC tool
### Create BatPaC instance


```python
batpac_excel = BatpacTool(
    BATPY_BATPAC_EXCEL,
    datasets.get_batpy_dataset("batpy_batpac_user_input_cells"),
    None,
    False,
)

```

### Add batteries to BatPaC object


```python
batpac_excel.add_battery(
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

```

## Brightway2 connector
### Create brightway2 instance


```python
brightway_excel = BrightwayConnector(BRIGHTWAY2_EXCEL, False)

```

### Load brightway2 configuration and export BatPaC battery data into brightway2 Excel


```python
brightway_excel.load_batpac_to_brightway_configuration(BRIGHTWAY_CONFIG)

brightway_excel.export_batpac_battery_to_brightway(
    batpac=batpac_excel,
    battery=bat1,
    batpac_config=batpy_batpac_dataset,
)
```

## Save Excel file


```python
brightway_excel.save()
```

## Close Excel file


```python
batpac_excel.close()
brightway_excel.close()
```




    True
