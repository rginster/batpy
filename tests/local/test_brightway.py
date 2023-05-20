# -*- coding: UTF-8 -*-
"""Tests for module batpac_brightway
"""

import pathlib

import pytest
import xlwings as xw

from batpy import datasets, utility_functions
from batpy.batpac_battery import BatpacBattery
from batpy.batpac_tool import BatpacTool
from batpy.brightway import BrightwayConnector

BATPY_BATPAC_EXCEL = "./tests/data/test_batpac.xlsm"
BATPY_BRIGHTWAY_EXCEL = "./tests/data/test_BatPaC-Brightway.xlsx"
BATPY_BRIGHTWAY_CONFIG = "./tests/data/test_batpy_batpac2brightway.toml"


def test_brightway_connector():
    """Test for BrightwayConnector"""
    brightway2_config = datasets.get_batpy_dataset("batpy_batpac2brightway")
    batpy_batpac_dataset = utility_functions.combine_configuration(
        [
            datasets.get_batpy_dataset("batpy_batpac_battery_design"),
            datasets.get_batpy_dataset("batpy_batpac_summary_of_results"),
        ]
    )

    bat1 = BatpacBattery("Battery 1")
    bat2 = BatpacBattery("Battery 2")
    bat3 = BatpacBattery("Battery 3")
    bat4 = BatpacBattery("Battery 4")
    bat5 = BatpacBattery("Battery 5")
    bat6 = BatpacBattery("Battery 6")
    bat7 = BatpacBattery("Battery 7")
    bat8 = BatpacBattery("Battery 8")

    battery_calculation = BatpacTool(
        BATPY_BATPAC_EXCEL,
        datasets.get_batpy_dataset("batpy_batpac_user_input_cells"),
        excel_visible=True,
    )

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

    brightway_connector = BrightwayConnector(BATPY_BRIGHTWAY_EXCEL, False)
    with pytest.raises(KeyError):
        brightway_connector.export_batpac_battery_to_brightway(
            batpac=battery_calculation,
            battery=bat1,
            batpac_config=batpy_batpac_dataset,
        )

    brightway_connector.load_batpac_to_brightway_configuration(
        brightway2_config
    )

    brightway_connector.load_batpac_to_brightway_configuration(
        BATPY_BRIGHTWAY_CONFIG
    )

    brightway_connector.export_batpac_battery_to_brightway(
        batpac=battery_calculation,
        battery=bat1,
        batpac_config=batpy_batpac_dataset,
    )

    assert (
        brightway_connector._read_value_direct(  # pylint: disable=W0212
            "Module", "B23"
        )
        == 15
    )
    assert (
        brightway_connector._read_value_direct(  # pylint: disable=W0212
            "Module", "B24"
        )
        == 20
    )
    with pytest.raises(KeyError):
        brightway_connector._read_value_direct(  # pylint: disable=W0212
            "42", "42"
        )

    with pytest.raises(KeyError):
        brightway_connector.export_batpac_battery_to_brightway(
            batpac=battery_calculation,
            battery=bat8,
            batpac_config=batpy_batpac_dataset,
        )

    path_saved_brightway = pathlib.Path(
        "./tests/saved_test_BatPaC-Brightway.xlsx"
    )
    assert not path_saved_brightway.is_file()

    brightway_connector.save(path_saved_brightway)
    assert path_saved_brightway.is_file()

    battery_calculation.close()
    assert brightway_connector.close()
    pathlib.Path.unlink(path_saved_brightway)

    brightway_connector = BrightwayConnector(BATPY_BRIGHTWAY_EXCEL, False)

    assert brightway_connector.close()

    brightway_connector = BrightwayConnector(BATPY_BRIGHTWAY_EXCEL, False)

    brightway_connector.workbook.close()
    del brightway_connector

    brightway_connector = BrightwayConnector(BATPY_BRIGHTWAY_EXCEL, False)

    xw.Book()
    assert brightway_connector.close()
    for app in xw.apps:
        app.quit()
