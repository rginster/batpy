# Example usage of BatPy
`batpy` is able to read, write, and calculate batteries in the BatPaC tool. To use `batpy` in a project. In order to use `batpy`in a project for BatPaC tool interaction, follow the example below.

## Import


```python
# included datasets
from batpy import datasets

# batpac battery and tool classes
from batpy.batpac_battery import BatpacBattery
from batpy.batpac_tool import BatpacTool

# pathlib for filesystem path handling
from pathlib import Path

```

## Paths to Excel file and to TOML configuration


```python
# Get BatPaC: https://www.anl.gov/partnerships/batpac-battery-manufacturing-cost-estimation
BATPY_BATPAC_EXCEL = Path("./example_data/excel_workbooks/dummy_BatPaC.xlsx")

# BatPaC battery configuration
BATPY_BATPAC_BATTERY_CONFIG = Path(
    "./example_data/conf_batpac/batpy_batteries_config.toml"
)
```

## Get included datasets

Show available dataset versions:


```python
datasets.get_available_batpy_dataset_versions()

```




    [Version('0.3.0'), Version('0.0.0'), Version('0.1.0')]



Show latest version:


```python
datasets.get_latest_batpy_dataset_version()
```




    Version('0.3.0')



Show available dataset of specified version and their description (default latest):


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
datasets.copy_integrated_dataset(
    "batpy_batteries_config", BATPY_BATPAC_BATTERY_CONFIG
)
```

Load included datasets:


```python
batpy_batpac_battery_design = datasets.get_batpy_dataset(
    "batpy_batpac_battery_design"
)
batpy_batpac_user_input_config = datasets.get_batpy_dataset(
    "batpy_batpac_user_input_cells"
)

batpy_batpac_tool_config = datasets.get_batpy_dataset("batpy_batpac_config")

batpy_batpac_tool_calculation_validation_config = datasets.get_batpy_dataset(
    "batpy_batpac_calculation_and_validation_results"
)

additional_user_defined_results_cells = datasets.get_batpy_dataset(
    "batpy_batpac_summary_of_results"
)
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

### Change battery properties
a) Write individual properties for created batteries


```python
bat1.set_new_property("Dashboard", "Number of modules in parallel", 10)

```

b) Load individiual battery configuration from file


```python
bat2.load_battery_file(BATPY_BATPAC_BATTERY_CONFIG, "Battery 2")

```




    True



## BatPaC tool
### Create BatPaC instance


```python
batpac_excel = BatpacTool(
    BATPY_BATPAC_EXCEL,
    batpy_batpac_user_input_config,
    batpy_batpac_tool_calculation_validation_config,
    workbook_visible=False,
)

```

### Add batteries to BatPaC object
a) Add individual batteries


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

b) Add individual batteries and load their configuration file (will overwrite all batteries)


```python
batpac_excel.load_batteries_file(
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

```

### Load configuration file for BatPaC instance


```python
batpac_excel.load_batpac_file(batpy_batpac_tool_config)

```

### Write configuration in Excel file and calculate batteries


```python
batpac_excel.calculate()

```

    Processing BatPaC configuration in each sheet: 100%|██████████| 7/7 [00:26<00:00,  3.73s/it]
    Processing battery configuration in each sheet: 100%|██████████| 5/5 [00:11<00:00,  2.26s/it]


### Print calculation and validation results


```python
batpac_excel.read_calculation_and_validation_results()

```

    +----------------------------------------------+-----------------------------+-----------------------------+-----------------------------+-----------------------------+-----------------------------+-----------------------------+-----------------------------+
    | Parameter                                    |          Battery 1          |          Battery 2          |          Battery 3          |          Battery 4          |          Battery 5          |          Battery 6          |          Battery 7          |
    +----------------------------------------------+-----------------------------+-----------------------------+-----------------------------+-----------------------------+-----------------------------+-----------------------------+-----------------------------+
    | Configuration Errors (see table to right)    |          1, 2, 3, 4         |           2, 3, 4           |             3, 4            |             3, 4            |             3, 4            |             3, 4            |             3, 4            |
    | Configuration Warnings (see table  to right) |             6, 7            |             6, 7            |              7              |              7              |              7              |              7              |              7              |
    | Plant Size, GWh                              |             15.0            |             20.0            |             25.0            |             30.0            |             35.0            |             40.0            |             45.0            |
    | Power-to-energy ratio                        |      3.3333333333333335     |             5.0             |             6.0             |      6.666666666666667      |      7.142857142857143      |             7.5             |      7.777777777777778      |
    | Adequacy of cooling                          |             None            |             Poor            |          Excellent          |          Excellent          |          Excellent          |          Excellent          |          Excellent          |
    | Cathode thickness limited by                 | Positive Thickness Override | Positive Thickness Override | Positive Thickness Override | Positive Thickness Override | Positive Thickness Override | Positive Thickness Override | Positive Thickness Override |
    +----------------------------------------------+-----------------------------+-----------------------------+-----------------------------+-----------------------------+-----------------------------+-----------------------------+-----------------------------+





    {'Parameter': ['Battery 1',
      'Battery 2',
      'Battery 3',
      'Battery 4',
      'Battery 5',
      'Battery 6',
      'Battery 7'],
     'Configuration Errors (see table to right)': ['1, 2, 3, 4',
      '2, 3, 4',
      '3, 4',
      '3, 4',
      '3, 4',
      '3, 4',
      '3, 4'],
     'Configuration Warnings (see table  to right)': ['6, 7',
      '6, 7',
      '7',
      '7',
      '7',
      '7',
      '7'],
     'Plant Size, GWh': [15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0],
     'Power-to-energy ratio': [3.3333333333333335,
      5.0,
      6.0,
      6.666666666666667,
      7.142857142857143,
      7.5,
      7.777777777777778],
     'Adequacy of cooling': [None,
      'Poor',
      'Excellent',
      'Excellent',
      'Excellent',
      'Excellent',
      'Excellent'],
     'Cathode thickness limited by': ['Positive Thickness Override',
      'Positive Thickness Override',
      'Positive Thickness Override',
      'Positive Thickness Override',
      'Positive Thickness Override',
      'Positive Thickness Override',
      'Positive Thickness Override']}



### Read additional cells


```python
user_results = batpac_excel.read_from_user_input(
    additional_user_defined_results_cells
)
```


```python
user_results["Summary of Results"]["Battery 1"]

```




    {'Battery System Parameters, Battery System Configuration and Performance, Number of battery packs': 1.0,
     'Battery System Parameters, Battery System Configuration and Performance, Packs in series or parallel': ' ',
     'Battery System Parameters, Battery System Configuration and Performance, Battery system average OCV, V': 0.017396678537706666,
     'Battery System Parameters, Battery System Configuration and Performance, Battery system nominal operating voltage, V': 0.017394939930528,
     'Battery System Parameters, Battery System Configuration and Performance, Battery system capacity, Ah': 1.0,
     'Battery System Parameters, Battery System Configuration and Performance, Battery system total energy, kWh': 1.7394939930528e-05,
     'Battery System Parameters, Battery System Configuration and Performance, Battery system useable energy, kWh(Useable)': 1.4785698940948799e-05,
     'Battery System Parameters, Battery System Configuration and Performance, Battery system power at target % OCV, kW': None,
     'Battery System Parameters, Battery System Configuration and Performance, Battery system rated power, kW': None,
     'Battery System Parameters, Battery System Configuration and Performance, Target SOC at full power, %': 20.0,
     'Battery System Parameters, Battery System Configuration and Performance, Pulse time at rated power, s': 10.0,
     'Battery System Parameters, Battery System Configuration and Performance, % OCV at rated power (adjusted for thickness limit), %': 80.0,
     'Battery System Parameters, Battery System Configuration and Performance, Cooling system power requirement, W': 0.8000000041377129,
     'Battery System Parameters, Battery System Size, Battery system volume (all packs and cooling), L': 3.39785056178627,
     'Battery System Parameters, Battery System Size, Battery system mass (all packs and cooling), kg': 7460.178966688378,
     'Battery System Parameters, Battery System Metrics, Battery system energy density, Wh/L': 0.005119395221837943,
     'Battery System Parameters, Battery System Metrics, Battery system specific energy, Wh/kg': 2.331705446772911e-06,
     'Battery System Parameters, Battery System Metrics, Battery system useable energy density, Wh(Useable)/L': 0.004351485938562251,
     'Battery System Parameters, Battery System Metrics, Battery system useable specific energy, Wh(Useable)/kg': 1.9819496297569742e-06,
     'Pack Parameters, Pack Configuration and Performance, Number of cells per pack': 100.0,
     'Pack Parameters, Pack Configuration and Performance, Number of modules per pack': 20.0,
     'Pack Parameters, Pack Configuration and Performance, Pack average OCV, V': 0.017396678537706666,
     'Pack Parameters, Pack Configuration and Performance, Pack nominal operating voltage, V': 0.017394939930528,
     'Pack Parameters, Pack Configuration and Performance, Pack capacity, Ah': 1.0,
     'Pack Parameters, Pack Configuration and Performance, Pack total energy, kWh': 1.7394939930528e-05,
     'Pack Parameters, Pack Configuration and Performance, Pack useable energy, kWh(Useable)': 1.4785698940948799e-05,
     'Pack Parameters, Pack Configuration and Performance, Pack power at target %OCV, kW': None,
     'Pack Parameters, Pack Configuration and Performance, Pack power at rated power, kW': None,
     'Pack Parameters, Pack Size, Pack length, mm': 135.8,
     'Pack Parameters, Pack Size, Pack width, mm': 238.66677826335894,
     'Pack Parameters, Pack Size, Pack height, mm': 46.60556485527991,
     'Pack Parameters, Pack Size, Pack volume, L': 2.59785056178627,
     'Pack Parameters, Pack Size, Pack total mass, kg': 7458.178966688378,
     'Pack Parameters, Pack Metrics, Pack power to energy ratio (with respect to power at target %OCV)': None,
     'Pack Parameters, Pack Metrics, Pack power to energy ratio (with respect to rated power)': None,
     'Pack Parameters, Pack Metrics, Pack energy density, Wh/L': 0.006695897056744988,
     'Pack Parameters, Pack Metrics, Pack specific energy, Wh/kg': 2.332330721510133e-06,
     'Pack Parameters, Pack Metrics, Pack useable energy density, Wh(Useable)/L': 0.005691512498233239,
     'Pack Parameters, Pack Metrics, Pack useable specific energy, Wh(Useable)/kg': 1.9824811132836125e-06,
     'Module Parameters, Module Configuration and Performance, Number of cells per module': 5.0,
     'Module Parameters, Module Configuration and Performance, Module average OCV, V': 8.698339268853333,
     'Module Parameters, Module Configuration and Performance, Module nominal operating voltage, V': 8.697469965264,
     'Module Parameters, Module Configuration and Performance, Module capacity, Ah': 0.0001,
     'Module Parameters, Module Configuration and Performance, Module total energy, kWh': 8.697469965264001e-07,
     'Module Parameters, Module Configuration and Performance, Module useable energy, kWh(Useable)': 7.392849470474401e-07,
     'Module Parameters, Module Configuration and Performance, Module power at target %OCV, kW': None,
     'Module Parameters, Module Configuration and Performance, Module power at rated power, kW': 5.0,
     'Module Parameters, Module Size, Module length, mm': 39.416694565839734,
     'Module Parameters, Module Size, Module width, mm': 7.6,
     'Module Parameters, Module Size, Module height, mm': 6.405564855279912,
     'Module Parameters, Module Size, Module volume, L': 0.001918895070009067,
     'Module Parameters, Module Size, Module volume per pack, L': 0.03837790140018134,
     'Module Parameters, Module Size, Module mass, kg': 0.24930163267098202,
     'Module Parameters, Module Size, Module mass per pack, kg': None,
     'Module Parameters, Module Metrics, Module energy density, Wh/L': 0.4532540679893927,
     'Module Parameters, Module Metrics, Module specific energy, Wh/kg': 0.0034887336565270557,
     'Module Parameters, Module Metrics, Module useable energy density, Wh(Useable)/L': 0.38526595779098377,
     'Module Parameters, Module Metrics, Module useable specific energy, Wh(Useable)/kg': 0.002965423608047998,
     'Cell Parameters, Cell Performance, Cell average OCV, V': 3.4793357075413334,
     'Cell Parameters, Cell Performance, Cell nominal operating voltage, V': 3.4789879861056,
     'Cell Parameters, Cell Performance, Cell capacity, Ah': 5e-05,
     'Cell Parameters, Cell Performance, Cell total energy, kWh': 1.7394939930528003e-07,
     'Cell Parameters, Cell Performance, Cell useable energy, kWh(Useable)': 1.4785698940948803e-07,
     'Cell Parameters, Cell Performance, Cell power at target %OCV, kW': None,
     'Cell Parameters, Cell Performance, Cell power at rated power, kW': 1.0,
     'Cell Parameters, Cell Size,Cell length, mm': 31.416694565839737,
     'Cell Parameters, Cell Size,Cell width, mm': 5.005564855279912,
     'Cell Parameters, Cell Size,Cell thickness, mm': 1.0,
     'Cell Parameters, Cell Size,Cell volume, L': 0.0001572583021878308,
     'Cell Parameters, Cell Size,Cell volume per pack, L': 0.015725830218783078,
     'Cell Parameters, Cell Size,Cell mass, kg': 0.005592130604280419,
     'Cell Parameters, Cell Size,Cell mass per pack, kg': 0.5592130604280419,
     'Cell Parameters, Cell Metrics, Cell energy density, Wh/L': 1.1061380981813806,
     'Cell Parameters, Cell Metrics, Cell specific energy, Wh/kg': 0.031106104562746234,
     'Cell Parameters, Cell Metrics, Cell useable energy density, Wh(Useable)/L': 0.9402173834541737,
     'Cell Parameters, Cell Metrics, Cell useable specific energy, Wh(Useable)/kg': 0.026440188878334308,
     'Cell Parameters, Additional Cell Information, Positive electrode thickness, µm': 1.0,
     'Cell Parameters, Additional Cell Information, Negative electrode thickness, µm': 1.2708328050734725,
     'Cell Parameters, Additional Cell Information, Positive electode areal capacity, mAh/cm²': 0.06715929876651021,
     'Cell Parameters, Additional Cell Information, Negative electrode areal capacity, mAh/cm²': 0.07387522864316123,
     'Plant Size, GWh': 8.697469965264e-06,
     'Packs manufactured at 100% utilization (pack/year)': 500000.0,
     'Packs manufactured per year (packs/year)': 500000.0,
     'Modules manufactured per year (modules/year)': 10000000.0,
     'Accepted cells manufactured per year (cells/year)': 50000000.0,
     'Costs, Battery System, Battery system cost, $': 65591.16432778076,
     'Costs, Battery System, Battery system cost, $/kWh': 3770703698.301868,
     'Costs, Battery System, Battery system cost, $/kWh(Useable)': 4436121998.002197,
     'Costs, Pack, Pack cost, $/pack': 65551.16432778076,
     'Costs, Pack, Pack cost, $/kWh': 3768404179.0071907,
     'Costs, Pack, Pack cost, $/kWh(Useable)': 4433416681.18493,
     'Costs, Module, Module cost, $/module': 17.496735940381853,
     'Costs, Module, Module cost per pack, $/pack': 349.93471880763707,
     'Costs, Module, Module cost, $/kWh': 20117040.94439004,
     'Costs, Module, Module cost, $/kWh(Useable)': 23667106.99340005,
     'Costs, Cell, Cell cost, $/cell': 1.0621528456420808,
     'Costs, Cell, Cell cost, $/module': 5.310764228210404,
     'Costs, Cell, Cell cost, $/pack': 106.21528456420808,
     'Costs, Cell, Cell cost, $/kWh': 6106102.406125644,
     'Costs, Cell, Cell cost, $/kWh(Useable)': 7183649.889559581,
     'Costs, Additional Considerations, Module fraction of pack cost': 0.0053383448241717014,
     'Costs, Additional Considerations, Cell fraction of module cost': 0.30352885511367556,
     'Costs, Additional Considerations, Cell fraction of pack cost': 0.0016203416926828522}



### Save configuration from Excel


```python
batpac_excel.save_config(
    batpac_path="./example_data/conf_batpac/saved_batpac_config.toml",
    battery_path="./example_data/conf_batpac/saved_batteries_config.toml",
)

```

    Saving BatPaC config from each sheet: 100%|██████████| 7/7 [00:00<00:00, 19027.95it/s]
    Saving battery configuration for each battery: 100%|██████████| 7/7 [00:00<00:00, 10190.95it/s]


## Save Excel file


```python
batpac_excel.save("./example_data/excel_workbooks/saved_dummy_BatPaC.xlsx")

```

## Close Excel file


```python
batpac_excel.close()

```




    True
