# -*- coding: UTF-8 -*-
"""Module, which contains utility functions for batpy
"""
import logging
from pathlib import Path

import semantic_version
import toml


def load_configuration(configuration: Path | str) -> dict:
    """Load configuration

    Loads a single configuration from a TOML file, string or dictionary.

    Parameters
    ----------
    configuration : Path | str
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


def is_version_compatible(
    self_version: semantic_version.Version,
    version_to_check: semantic_version.Version,
    include_minor: bool = False,
) -> bool:
    """Check for version compatibility

    Check if two versions (major.minor.patch) are compatible. Thereby a version
    is compatible if major is equal. If minor should also be included a version
    is compatible if major is equal and minor is greater or equal.

    Parameters
    ----------
    self_version : semantic_version.Version
        Version
    version_to_check : semantic_version.Version
        Version to be checked against self_version.
    include_minor : bool, optional
        Check if minor version of version_to_check is greater or equal to
        self_version's minor, by default False.

    Returns
    -------
    bool
        True, if version is compatible.

    Raises
    ------
    ValueError
        If version is not compatible a ValueError will occur.
    """
    if include_minor:
        min_minor = self_version.minor
    else:
        min_minor = 0

    min_version = semantic_version.Version(
        major=self_version.major, minor=min_minor, patch=0
    )

    if min_version <= version_to_check < min_version.next_major():
        logging.info(
            "[+] Version %s is compatible: %s <= %s < %s",
            version_to_check,
            min_version,
            version_to_check,
            min_version.next_major(),
        )
        return True

    logging.warning(
        "[!] Version %s should be %s <= %s < %s",
        version_to_check,
        min_version,
        version_to_check,
        min_version.next_major(),
    )
    raise ValueError(
        f"[!] Version {version_to_check} should be {min_version} <=\
            {version_to_check} < {min_version.next_major()}"
    )


def combine_configuration(configuration_list: list[Path | str]) -> dict:
    """Combine configuration files

    Combines a list of configuration file into one configuration.

    Parameters
    ----------
    configuration_list : list[Path  |  str ]
        List of individual configurations. Thereby it is possible to combine
        different configuration types (path, str) with each other.

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
