# -*- coding: UTF-8 -*-
"""Module, which contains utility functions for batpy
"""
import logging
from pathlib import Path

import semantic_version
import toml

from batpy.is_version_compatible import is_version_compatible


def load_configuration(configuration: Path | str | dict) -> dict:
    """Load configuration

    Loads a single configuration from a TOML file, string or dictionary.

    Parameters
    ----------
    configuration : Path | str | dict
        Path to the TOML configuration file or configuration as string or
        dictionary.

    Returns
    -------
    dict
        Returns dictionary representation of configuration.
    """
    logging.info("[ ] Load configuration from %s", configuration)
    try:
        Path.exists(Path(configuration))
        config = toml.load(configuration)
    except (AttributeError, OSError):
        config = toml.loads(configuration)
    logging.info("[+] Loaded configuration from %s", configuration)
    logging.debug("[ ] Config properties %s", config)
    return config


def combine_configuration(configuration_list: list[Path | str | dict]) -> dict:
    """Combine configuration files
    Combines a list of configuration file into one configuration.

    Parameters
    ----------
    configuration_list : list[Path  |  str  |  dict]
        List of individual configurations. Thereby it is possible to combine
        different configuration types (path, str, dict) with each other.

    Returns
    -------
    dict
        Combined configuration
    """
    combined_configuration = {}
    version = None
    for configuration in configuration_list:
        config = load_configuration(configuration)
        config_metadata = config.pop("batpy")
        if version:
            is_version_compatible(
                version,
                semantic_version.Version(config_metadata["BatPaC SemVer"]),
            )
        else:
            version = semantic_version.Version(
                config_metadata["BatPaC SemVer"]
            )
        combined_configuration |= config
    return combined_configuration
