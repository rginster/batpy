# pylint: disable=W0621, W0613, W0611, E0401, W0212
# -*- coding: UTF-8 -*-
"""Tests for module batpac_tool
"""
import pathlib

import pytest
import semantic_version
import toml
import xlwings as xw
from data.batpy_test_data_batpac_tool import example_batpac_data  # noqa: F401
from data.batpy_test_data_battery import example_battery_data  # noqa: F401

from batpy import batpac_datasets
from batpy.batpac_battery import BatpacBattery
from batpy.batpac_tool import BatpacTool

BATPY_BATPAC_BATTERY_CONFIG = batpac_datasets.get_batpy_dataset(
    "batpy_batteries_config", "0.0.0"
)

BATPY_BATPAC_BATTERY_CONFIG_PATH = (
    "./src/batpy/data/0.0.0/batpy_batteries_config.toml"
)

BATPY_BATPAC_USER_INPUT_CONFIG = batpac_datasets.get_batpy_dataset(
    "batpy_batpac_user_input_cells.toml", "0.0.0"
)

BATPY_BATPAC_USER_INPUT_CONFIG_PATH = (
    "./src/batpy/data/0.0.0/batpy_batpac_user_input_cells.toml"
)

BATPY_BATPAC_TOOL_CONFIG = batpac_datasets.get_batpy_dataset(
    "batpy_batpac_config.toml", "0.0.0"
)

BATPY_BATPAC_TOOL_CONFIG_PATH = (
    "./src/batpy/data/0.0.0/batpy_batpac_config.toml"
)

BATPY_BATPAC_TOOL_CALCULATION_VALIDATION_CONFIG = (
    batpac_datasets.get_batpy_dataset(
        "batpy_batpac_calculation_and_validation_results.toml", "0.0.0"
    )
)

BATPY_BATPAC_TOOL_CALCULATION_VALIDATION_CONFIG_PATH = pathlib.Path(
    "./src/batpy/data",
    "0.0.0/batpy_batpac_calculation_and_validation_results.toml",
)
BATPY_BATPAC_EXCEL = "./tests/data/test_batpac.xlsm"


# Tests for BatPaC class
def test_create_batpac():
    """Test create_batpac"""
    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH,
    )
    config = toml.load(BATPY_BATPAC_USER_INPUT_CONFIG_PATH)
    config.pop("batpy")
    # assert test_batpac.workbook_path == BATPY_BATPAC_EXCEL
    # assert test_batpac.toml_path == BATPY_BATPAC_USER_INPUT_CONFIG_PATH
    assert test_batpac.excel_cells == config
    # assert test_batpac.batpac_version == config_metadata["BatPaC version"]
    assert not test_batpac.batteries
    assert not test_batpac.properties
    # assert test_batpac.reset_macro == test_batpac.wb.macro("Module1.Reset")
    assert test_batpac.workbook.fullname in [i.fullname for i in xw.books]

    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG,
    )
    config = toml.load(BATPY_BATPAC_USER_INPUT_CONFIG_PATH)
    config.pop("batpy")
    # assert test_batpac.workbook_path == BATPY_BATPAC_EXCEL
    # assert test_batpac.toml_path == BATPY_BATPAC_USER_INPUT_CONFIG_PATH
    assert test_batpac.excel_cells == config
    # assert test_batpac.batpac_version == config_metadata["BatPaC version"]
    assert not test_batpac.batteries
    assert not test_batpac.properties
    # assert test_batpac.reset_macro == test_batpac.wb.macro("Module1.Reset")
    assert test_batpac.workbook.fullname in [i.fullname for i in xw.books]


def test_load_batpac(example_batpac_data):  # noqa: F811
    """Test load_batpac

    Parameters
    ----------
    example_batpac_data : _type_
        Example batpac data for validation
    """
    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH,
    )
    test_batpac.load_batpac_file(BATPY_BATPAC_TOOL_CONFIG_PATH)
    assert test_batpac.properties == example_batpac_data
    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH,
    )
    test_batpac.load_batpac_file(BATPY_BATPAC_TOOL_CONFIG)
    assert test_batpac.properties == example_batpac_data


def test_add_battery():
    """Test add_battery"""
    test_bat1 = BatpacBattery("Battery 1")
    test_bat2 = BatpacBattery("Battery 2")
    test_bat3 = BatpacBattery("Battery 3")
    test_bat4 = BatpacBattery("Battery 4")
    test_bat5 = BatpacBattery("Battery 5")
    test_bat6 = BatpacBattery("Battery 6")
    test_bat7 = BatpacBattery("Battery 7")
    test_bat8 = BatpacBattery("Battery 8")
    test_bat9 = BatpacBattery("Battery 9")

    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH,
    )

    test_batpac.add_battery(
        [
            test_bat1,
            test_bat2,
            test_bat3,
            test_bat4,
            test_bat5,
            test_bat6,
            test_bat7,
        ]
    )
    assert test_batpac.batteries == [
        test_bat1,
        test_bat2,
        test_bat3,
        test_bat4,
        test_bat5,
        test_bat6,
        test_bat7,
    ]

    test_batpac.add_battery(
        [
            test_bat8,
            test_bat9,
            test_bat3,
            test_bat4,
            test_bat5,
            test_bat6,
            test_bat7,
            test_bat1,
            test_bat2,
        ]
    )
    assert test_batpac.batteries != [
        test_bat8,
        test_bat9,
        test_bat3,
        test_bat4,
        test_bat5,
        test_bat6,
        test_bat7,
    ]
    test_batpac.batteries.clear()
    test_batpac.add_battery(
        [
            test_bat8,
            test_bat9,
            test_bat3,
            test_bat4,
            test_bat5,
            test_bat6,
            test_bat7,
            test_bat1,
            test_bat2,
        ]
    )
    assert test_batpac.batteries == [
        test_bat8,
        test_bat9,
        test_bat3,
        test_bat4,
        test_bat5,
        test_bat6,
        test_bat7,
    ]


def test_load_batteries_file(example_battery_data):  # noqa: F811
    """Test load_batteries_file

    Parameters
    ----------
    example_battery_data : _type_
        Example battery data for validation
    """
    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH,
    )
    test_bat1 = BatpacBattery("Battery 1")
    test_bat2 = BatpacBattery("Battery 2")
    test_bat3 = BatpacBattery("Battery 3")
    test_bat4 = BatpacBattery("Battery 4")
    test_bat5 = BatpacBattery("Battery 5")
    test_bat6 = BatpacBattery("Battery 6")
    test_bat7 = BatpacBattery("Battery 7")

    test_batpac.load_batteries_file(
        BATPY_BATPAC_BATTERY_CONFIG_PATH,
        [
            test_bat1,
            test_bat2,
            test_bat3,
            test_bat4,
            test_bat5,
            test_bat6,
            test_bat7,
        ],
    )
    assert test_batpac.batteries[1].properties == example_battery_data

    test_batpac.load_batteries_file(
        BATPY_BATPAC_BATTERY_CONFIG,
        [
            test_bat1,
            test_bat2,
            test_bat3,
            test_bat4,
            test_bat5,
            test_bat6,
            test_bat7,
        ],
    )
    assert test_batpac.batteries[1].properties == example_battery_data


def test_write_read_value_direct():
    """Test write_read_value_direct"""
    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH,
    )
    test_batpac._write_value_direct("Dashboard", "A1", True)
    assert test_batpac._read_value_direct("Dashboard", "A1")
    test_batpac._write_value_direct("Dashboard", "A1", None)
    assert test_batpac._read_value_direct("Dashboard", "A1") is None
    with pytest.raises(KeyError):
        assert test_batpac._read_value_direct("no sheet", "no name")


def test_wb_helper_range():
    """Test wb_helper_range"""
    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH,
    )
    test_bat1 = BatpacBattery("Battery 1")
    test_batpac.add_battery([test_bat1])
    assert test_batpac._wb_helper_range("Dashboard", "Restart (0/1)") == "D6"
    assert (
        test_batpac._wb_helper_range(
            "Dashboard", "Target rated peak power of pack, kW", test_bat1
        )
        == "D38"
    )
    with pytest.raises(KeyError):
        additional_cell_config = (
            BATPY_BATPAC_TOOL_CALCULATION_VALIDATION_CONFIG_PATH,
        )

        assert test_batpac._wb_helper_range(
            "no sheet",
            "no name",
            battery=None,
            additional_cell_config=additional_cell_config,
        )


def test_write_read_value():
    """Test write_read_value"""
    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH,
    )
    test_bat1 = BatpacBattery("Battery 1")
    test_batpac.add_battery([test_bat1])

    test_batpac.write_value("Dashboard", "Restart (0/1)", 0)
    assert test_batpac.read_value("Dashboard", "Restart (0/1)") == 0

    test_batpac.write_value_battery(
        "Dashboard", "Target rated peak power of pack, kW", test_bat1, True
    )
    assert test_batpac.read_value_battery(
        "Dashboard", "Target rated peak power of pack, kW", test_bat1
    )

    test_batpac.write_value_battery(
        "Dashboard", "Target rated peak power of pack, kW", test_bat1, 100
    )
    assert (
        test_batpac.read_value_battery(
            "Dashboard", "Target rated peak power of pack, kW", test_bat1
        )
        == 100
    )
    with pytest.raises(KeyError):
        assert test_batpac.read_value("no sheet", "no name", {})

    test_batpac.write_value("Dashboard", "Restart (0/1)", 1)
    assert test_batpac.read_value("Dashboard", "Restart (0/1)") == 1


def test_stop_automatic_calculation():
    """Test stop_automatic_calculation"""
    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH,
    )
    test_batpac.stop_automatic_calculation()
    assert test_batpac.read_value("Dashboard", "Restart (0/1)") == 0


def test_is_version_compatible():
    """Test is_version_compatible"""
    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH,
    )
    version_to_compare = semantic_version.Version("5.4.3")

    test_batpac.version = semantic_version.Version("5.0.0")
    assert test_batpac.is_version_compatible(version_to_compare)

    with pytest.raises(ValueError):
        test_batpac.version = semantic_version.Version("100.0.0")
        assert test_batpac.is_version_compatible(version_to_compare)

    with pytest.raises(ValueError):
        test_batpac.version = semantic_version.Version("4.0.0")
        assert test_batpac.is_version_compatible(version_to_compare)

    with pytest.raises(ValueError):
        test_batpac.version = semantic_version.Version("5.100.0")
        assert test_batpac.is_version_compatible(
            version_to_compare, include_minor=True
        )


def test_start_automatic_calculation():
    """Test start_automatic_calculation"""
    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH,
    )
    test_batpac.start_automatic_calculation()
    assert test_batpac.read_value("Dashboard", "Restart (0/1)") == 1


def test_read_from_user_input(example_battery_data):  # noqa: F811
    """Test from_user_input"""
    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG,
        BATPY_BATPAC_TOOL_CALCULATION_VALIDATION_CONFIG,
    )
    test_bat1 = BatpacBattery("Battery 1")
    test_bat2 = BatpacBattery("Battery 2")
    test_bat3 = BatpacBattery("Battery 3")
    test_bat4 = BatpacBattery("Battery 4")
    test_bat5 = BatpacBattery("Battery 5")
    test_bat6 = BatpacBattery("Battery 6")
    test_bat7 = BatpacBattery("Battery 7")

    test_batpac.load_batteries_file(
        BATPY_BATPAC_BATTERY_CONFIG_PATH,
        [
            test_bat1,
            test_bat2,
            test_bat3,
            test_bat4,
            test_bat5,
            test_bat6,
            test_bat7,
        ],
    )
    test_batpac.load_batpac_file(BATPY_BATPAC_TOOL_CONFIG)
    test_batpac.calculate()
    for sheet in test_batpac.batteries[0].properties:
        for key, value in test_batpac.batteries[0].properties[sheet].items():
            assert (
                test_batpac.read_value_battery(sheet, key, test_bat1) == value
            )

    validation = test_batpac.read_from_user_input(
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH
    )
    validation_result = example_battery_data
    assert (
        validation_result["Dashboard"] == validation["Dashboard"]["Battery 2"]
    )


def test_save_config(example_battery_data):  # noqa: F811
    """Test save_config

    Parameters
    ----------
    example_battery_data : _type_
        Example battery data for validation
    """
    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH,
    )
    test_bat1 = BatpacBattery("Battery 1")
    test_bat2 = BatpacBattery("Battery 2")
    test_bat3 = BatpacBattery("Battery 3")
    test_bat4 = BatpacBattery("Battery 4")
    test_bat5 = BatpacBattery("Battery 5")
    test_bat6 = BatpacBattery("Battery 6")
    test_bat7 = BatpacBattery("Battery 7")

    test_batpac.add_battery(
        [
            test_bat1,
            test_bat2,
            test_bat3,
            test_bat4,
            test_bat5,
            test_bat6,
            test_bat7,
        ],
    )
    assert test_batpac.properties == {}
    for battery in test_batpac.batteries:
        assert battery.properties == {}

    assert test_bat2.load_battery_file(
        BATPY_BATPAC_BATTERY_CONFIG_PATH, test_bat2.name
    )
    properties = example_battery_data
    assert properties == test_bat2.properties
    test_batpac.calculate()
    test_batpac.batteries[5].set_new_property("new", "new", "new")
    test_batpac.save_config()
    assert test_batpac.properties != {}
    for battery in test_batpac.batteries:
        assert battery.properties != {}
        if battery.name == "Battery 2":
            assert battery.properties == example_battery_data

    path_saved_batpac = pathlib.Path("./tests/saved_test_batpac_config.toml")
    assert not path_saved_batpac.is_file()

    path_saved_batteries = pathlib.Path(
        "./tests/saved_test_batteries_config.toml"
    )
    assert not path_saved_batteries.is_file()

    test_batpac.save_config(path_saved_batpac, path_saved_batteries)
    assert test_batpac.properties != {}
    for battery in test_batpac.batteries:
        assert battery.properties != {}
        if battery.name == "Battery 2":
            assert battery.properties == example_battery_data

    assert path_saved_batpac.is_file()
    assert path_saved_batteries.is_file()

    pathlib.Path.unlink(path_saved_batpac)
    pathlib.Path.unlink(path_saved_batteries)


def test_read_calculation_and_validation_results():
    """Test read_calculation_and_validation_results"""
    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH,
        BATPY_BATPAC_TOOL_CALCULATION_VALIDATION_CONFIG_PATH,
    )
    test_bat1 = BatpacBattery("Battery 1")
    test_bat2 = BatpacBattery("Battery 2")
    test_bat3 = BatpacBattery("Battery 3")
    test_bat4 = BatpacBattery("Battery 4")
    test_bat5 = BatpacBattery("Battery 5")
    test_bat6 = BatpacBattery("Battery 6")
    test_bat7 = BatpacBattery("Battery 7")

    test_batpac.load_batteries_file(
        BATPY_BATPAC_BATTERY_CONFIG_PATH,
        [
            test_bat1,
            test_bat2,
            test_bat3,
            test_bat4,
            test_bat5,
            test_bat6,
            test_bat7,
        ],
    )
    test_batpac.load_batpac_file(BATPY_BATPAC_TOOL_CONFIG_PATH)
    test_batpac.calculate()

    validation_1 = test_batpac.read_calculation_and_validation_results()
    assert validation_1

    test_batpac.toml_calculation_validation_results = None
    with pytest.raises(KeyError):
        assert test_batpac.read_calculation_and_validation_results()

    validation_3 = test_batpac.read_calculation_and_validation_results(
        BATPY_BATPAC_TOOL_CALCULATION_VALIDATION_CONFIG_PATH
    )
    assert validation_3
    assert validation_1 == validation_3

    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG,
        BATPY_BATPAC_TOOL_CALCULATION_VALIDATION_CONFIG,
    )
    test_bat1 = BatpacBattery("Battery 1")
    test_bat2 = BatpacBattery("Battery 2")
    test_bat3 = BatpacBattery("Battery 3")
    test_bat4 = BatpacBattery("Battery 4")
    test_bat5 = BatpacBattery("Battery 5")
    test_bat6 = BatpacBattery("Battery 6")
    test_bat7 = BatpacBattery("Battery 7")

    test_batpac.load_batteries_file(
        BATPY_BATPAC_BATTERY_CONFIG_PATH,
        [
            test_bat1,
            test_bat2,
            test_bat3,
            test_bat4,
            test_bat5,
            test_bat6,
            test_bat7,
        ],
    )
    test_batpac.load_batpac_file(BATPY_BATPAC_TOOL_CONFIG)
    test_batpac.calculate()

    validation_1 = test_batpac.read_calculation_and_validation_results()
    assert validation_1

    test_batpac.toml_calculation_validation_results = None
    with pytest.raises(KeyError):
        assert test_batpac.read_calculation_and_validation_results()

    validation_3 = test_batpac.read_calculation_and_validation_results(
        BATPY_BATPAC_TOOL_CALCULATION_VALIDATION_CONFIG
    )
    assert validation_3
    assert validation_1 == validation_3


def test_save():
    """Test save"""
    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH,
    )
    path_saved_batpac = pathlib.Path("./tests/saved_test_batpac.xlsm")
    assert not path_saved_batpac.is_file()

    test_batpac.save(path_saved_batpac)
    assert path_saved_batpac.is_file()

    test_batpac.close()
    pathlib.Path.unlink(path_saved_batpac)

    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH,
    )
    path_saved_batpac = pathlib.Path(BATPY_BATPAC_EXCEL)
    test_batpac.save()
    assert path_saved_batpac.is_file()
    test_batpac.close()


def test_close_batpac():
    """Test close_batpac"""
    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH,
    )
    assert test_batpac.close()

    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH,
    )
    test_batpac.workbook.close()
    del test_batpac

    test_batpac = BatpacTool(
        BATPY_BATPAC_EXCEL,
        BATPY_BATPAC_USER_INPUT_CONFIG_PATH,
    )
    xw.Book()
    assert test_batpac.close()
    for app in xw.apps:
        app.quit()
