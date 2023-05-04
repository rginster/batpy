# -*- coding: UTF-8 -*-
"""Tests for module batpac_datasets
"""

import pytest
import semantic_version
import toml

from batpy import batpac_datasets, data

# from data.batpy_test_data import example_battery_data  # noqa: F401

LATEST_DATASET_VERSION = "0.1.0"


BATPY_BATPAC_TOOL_CONFIG = (
    f"./src/batpy/data/{LATEST_DATASET_VERSION}/batpy_batpac_config.toml"
)
BATPY_BATPAC_TOOL_CONFIG_VERSION = (
    "./src/batpy/data/0.0.0/batpy_batpac_config.toml"
)

AVAILABLE_DATASETS_0_0_0 = [
    "batpy_batpac_calculation_and_validation_results.toml",
    "batpy_batpac_config.toml",
    "batpy_batpac_user_input_cells.toml",
    "batpy_batteries_config.toml",
]


def test_get_batpy_dataset():
    """Test get_batpy_dataset"""

    config_file_version_str = batpac_datasets.get_batpy_dataset(
        "batpy_batpac_config", "0.0.0"
    )
    config_file_version = batpac_datasets.get_batpy_dataset(
        "batpy_batpac_config", semantic_version.Version("0.0.0")
    )
    config_file = batpac_datasets.get_batpy_dataset("batpy_batpac_config")
    config_file_toml = batpac_datasets.get_batpy_dataset(
        "batpy_batpac_config.toml"
    )
    config_file_version_empty = batpac_datasets.get_batpy_dataset(
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
        assert batpac_datasets.get_batpy_dataset("batpy_batpac_config_invalid")


def test_get_latest_batpy_dataset_version():
    """Test get_latest_batpy_dataset_version"""

    assert (
        batpac_datasets.get_latest_batpy_dataset_version()
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

    for (
        dataset_version
    ) in batpac_datasets.get_available_batpy_dataset_versions():
        assert dataset_version in available_dataset_versions


def test_get_available_batpy_dataset_names():
    """Test get_available_batpy_dataset_names"""

    for dataset_name in batpac_datasets.get_available_batpy_dataset_names(
        "0.0.0"
    ):
        assert dataset_name in AVAILABLE_DATASETS_0_0_0
