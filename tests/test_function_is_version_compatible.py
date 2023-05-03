# -*- coding: UTF-8 -*-
"""Tests for module is_version_compatible
"""

import pytest
import semantic_version

from batpy.is_version_compatible import is_version_compatible


def test_function_is_version_compatible():
    """Test function_is_version_compatible"""
    version_to_compare = semantic_version.Version("5.4.3")

    self_version = semantic_version.Version("5.0.0")
    assert is_version_compatible(self_version, version_to_compare)

    with pytest.raises(ValueError):
        self_version = semantic_version.Version("100.0.0")
        assert is_version_compatible(self_version, version_to_compare)

    with pytest.raises(ValueError):
        self_version = semantic_version.Version("4.0.0")
        assert is_version_compatible(self_version, version_to_compare)

    with pytest.raises(ValueError):
        self_version = semantic_version.Version("5.100.0")
        assert is_version_compatible(
            self_version, version_to_compare, include_minor=True
        )
