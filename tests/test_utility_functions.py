# -*- coding: UTF-8 -*-
"""Tests for module is_version_compatible
"""

import pytest
import semantic_version

from batpy import utility_functions

CONFIG_TO_COMBINE_1 = "./tests/data/test_batpac2brightway_1.toml"
CONFIG_TO_COMBINE_2 = "./tests/data/test_batpac2brightway_2.toml"


def test_is_version_compatible():
    """Test is_version_compatible"""

    version_to_compare = semantic_version.Version("5.4.3")

    self_version = semantic_version.Version("5.0.0")
    assert utility_functions.is_version_compatible(
        self_version, version_to_compare
    )

    with pytest.raises(ValueError):
        self_version = semantic_version.Version("100.0.0")
        assert utility_functions.is_version_compatible(
            self_version, version_to_compare
        )

    with pytest.raises(ValueError):
        self_version = semantic_version.Version("4.0.0")
        assert utility_functions.is_version_compatible(
            self_version, version_to_compare
        )

    with pytest.raises(ValueError):
        self_version = semantic_version.Version("5.100.0")
        assert utility_functions.is_version_compatible(
            self_version, version_to_compare, include_minor=True
        )


def test_load_configuration():
    """Test load_configuration"""

    dict_to_combine_1 = {
        "batpy": {
            "BatPaC version": "BatPaC 5.0 2022-07-22",
            "BatPaC SemVer": "0.1.0",
        },
        "Sheet 1": {"Cell name 1": "Cell range 1"},
    }
    dict_to_combine_2 = {
        "batpy": {
            "BatPaC version": "BatPaC 5.0 2022-07-22",
            "BatPaC SemVer": "0.1.0",
        },
        "Sheet 2": {"Cell name 2": "Cell range 2"},
    }
    assert dict_to_combine_1 == utility_functions.load_configuration(
        CONFIG_TO_COMBINE_1
    )
    assert dict_to_combine_2 == utility_functions.load_configuration(
        CONFIG_TO_COMBINE_2
    )


def test_combine_configuration():
    """Test combine_configuration"""

    combined_dict = {
        "Sheet 1": {"Cell name 1": "Cell range 1"},
        "Sheet 2": {"Cell name 2": "Cell range 2"},
    }

    assert combined_dict == utility_functions.combine_configuration(
        [CONFIG_TO_COMBINE_1, CONFIG_TO_COMBINE_2]
    )
