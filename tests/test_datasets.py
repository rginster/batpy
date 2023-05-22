# -*- coding: UTF-8 -*-
"""Tests for module batpac_datasets
"""

import pytest
import semantic_version
import toml

from batpy import data, datasets

# from data.batpy_test_data import example_battery_data  # noqa: F401

LATEST_DATASET_VERSION = "0.3.0"


BATPY_BATPAC_TOOL_CONFIG = (
    f"./src/batpy/data/{LATEST_DATASET_VERSION}/batpy_batpac_config.toml"
)
BATPY_BATPAC_TOOL_CONFIG_VERSION = (
    "./src/batpy/data/0.0.0/batpy_batpac_config.toml"
)

AVAILABLE_DATASETS_0_0_0 = [
    "batpy_batpac_battery_design.toml",
    "batpy_batpac_calculation_and_validation_results.toml",
    "batpy_batpac_config.toml",
    "batpy_batpac_summary_of_results.toml",
    "batpy_batpac_user_input_cells.toml",
    "batpy_batteries_config.toml",
]

DATASET_INFORMATION = (
    "Configuration for worksheet battery design in BatPaC Excel"
)


def test_get_batpy_dataset():
    """Test get_batpy_dataset"""

    config_file_version_str = datasets.get_batpy_dataset(
        "batpy_batpac_config", "0.0.0"
    )
    config_file_version = datasets.get_batpy_dataset(
        "batpy_batpac_config", semantic_version.Version("0.0.0")
    )
    config_file = datasets.get_batpy_dataset("batpy_batpac_config")
    config_file_toml = datasets.get_batpy_dataset("batpy_batpac_config.toml")
    config_file_version_empty = datasets.get_batpy_dataset(
        "batpy_batpac_config", ""
    )

    toml_from_path = toml.load(BATPY_BATPAC_TOOL_CONFIG)
    toml_from_path_version = toml.load(BATPY_BATPAC_TOOL_CONFIG_VERSION)

    assert toml.loads(config_file) == toml_from_path
    assert toml.loads(config_file_toml) == toml_from_path

    assert toml.loads(config_file_version_str) == toml_from_path_version
    assert toml.loads(config_file_version) == toml_from_path_version
    assert toml.loads(config_file_version_empty) == toml_from_path

    with pytest.raises(FileNotFoundError):
        assert datasets.get_batpy_dataset("batpy_batpac_config_invalid")


def test_get_latest_batpy_dataset_version():
    """Test get_latest_batpy_dataset_version"""

    assert (
        datasets.get_latest_batpy_dataset_version()
        == semantic_version.Version(LATEST_DATASET_VERSION)
    )


def test_get_available_batpy_dataset_versions():
    """Test get_available_batpy_dataset_versions"""
    available_dataset_versions = []
    for version_dir in data.__versions__:
        try:
            available_dataset_versions.append(
                semantic_version.Version(version_dir)
            )
        except ValueError:
            continue

    for dataset_version in datasets.get_available_batpy_dataset_versions():
        assert dataset_version in available_dataset_versions


def test_get_available_batpy_dataset_names():
    """Test get_available_batpy_dataset_names"""

    for dataset_name in datasets.get_available_batpy_dataset_names("0.0.0"):
        assert dataset_name in AVAILABLE_DATASETS_0_0_0
    assert datasets.get_available_batpy_dataset_names("")
    with pytest.raises(ValueError):
        assert datasets.get_available_batpy_dataset_names("42.42.42")


def test_get_available_batpy_datasets():
    """Test get_available_batpy_datasets"""
    dataset_dict = datasets.get_available_batpy_datasets()
    assert (
        dataset_dict["batpy_batpac_battery_design.toml"] == DATASET_INFORMATION
    )
    with pytest.raises(KeyError):
        dataset_dict = datasets.get_batpy_dataset(
            "batpy_batpac_battery_design"
        )
        dataset_dict = dataset_dict.replace(
            '"information"',
            '"information_"',
        )
        assert datasets.get_dataset_information(dataset_dict)
