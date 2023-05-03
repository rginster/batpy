# pylint: disable=W0621, W0613, W0611
# -*- coding: UTF-8 -*-
"""Tests for module batpac_battery
"""

import pytest
from data.batpy_test_data import example_battery_data  # noqa: F401

from batpy.batpac_battery import BatpacBattery

BATPY_BATPAC_BATTERY_CONFIG = "./src/batpy/data/batpy_batteries_config.toml"


@pytest.mark.parametrize(
    "battery_to_create, expected_battery_name",
    [
        ("Battery", "Battery"),
        ("Battery 2", "Battery 2"),
        ("NMC811 - G", "NMC811 - G"),
    ],
)
def test_create_battery_with_name(battery_to_create, expected_battery_name):
    """Test create_battery_with_name

    Parameters
    ----------
    battery_to_create : _type_
        Battery name for BatpacBattery object creation.
    expected_battery_name : _type_
        Expected battery name after object creation.
    """
    test_battery = BatpacBattery(battery_to_create)
    assert test_battery.name == expected_battery_name
    assert test_battery.properties == {}


def test_create_battery_without_name():
    """Test create_battery_without_name"""
    test_battery = BatpacBattery()
    assert test_battery.name == "Battery"
    assert test_battery.properties == {}


def test_load_battery_from_valid_file(example_battery_data):  # noqa: F811
    """Test load_battery_from_valid_file

    Parameters
    ----------
    example_battery_data : _type_
        Example battery properties for validation.
    """
    test_battery = BatpacBattery("Battery 2")
    assert test_battery.load_battery_file(
        BATPY_BATPAC_BATTERY_CONFIG, test_battery.name
    )
    properties = example_battery_data
    assert properties == test_battery.properties
    # print(example_battery_data )


def test_load_battery_from_invalid_file():
    """Test load_battery_from_invalid_file"""
    test_battery = BatpacBattery()
    assert not test_battery.load_battery_file(
        BATPY_BATPAC_BATTERY_CONFIG, test_battery.name
    )
    assert {} == test_battery.properties


def test_set_property(example_battery_data):  # noqa: F811
    """Test set_property

    Parameters
    ----------
    example_battery_data : _type_
        Example battery properties for validation.
    """
    test_battery = BatpacBattery()
    test_battery.properties = example_battery_data
    assert test_battery.properties == example_battery_data
    test_battery.set_property(
        "Dashboard", "Target rated peak power of pack, kW", 1
    )
    example_battery_data["Dashboard"][
        "Target rated peak power of pack, kW"
    ] = 1
    assert test_battery.properties == example_battery_data


def test_set_new_property(example_battery_data):  # noqa: F811
    """Test set_new_property

    Parameters
    ----------
    example_battery_data : _type_
        Example battery properties for validation.
    """
    test_battery = BatpacBattery()
    test_battery.set_new_property("new", "new", 1)
    test_property = {"new": {"new": 1}}
    assert test_battery.properties == test_property


def test_get_property():
    """Test get_property"""
    test_battery = BatpacBattery()
    test_battery.set_new_property("new", "new", 1)
    test_property = {"new": {"new": 1}}
    assert (
        test_battery.get_property("new", "new") == test_property["new"]["new"]
    )
