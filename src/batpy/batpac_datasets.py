# -*- coding: UTF-8 -*-
"""Module, to load default batpy datasets
"""

import logging
import os
from pkgutil import get_data

import semantic_version

from batpy import data

# from data import get_versions

# __versions__ =
# [f.name for f in os.scandir(__name__.__path__[0]) if f.is_dir()]

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s [%(levelname)s]: \t%(filename)s\t%(funcName)s\t\
        %(lineno)s\t- %(message)s",
    filename="batpy.log",
    filemode="w",
    level=logging.INFO,
)


def get_batpy_dataset(
    dataset_name: str, dataset_version: semantic_version.Version | str = None
) -> str:
    """Get included batpy dataset

    Parameters
    ----------
    dataset_name : str
        Name of included batpy dataset.
    dataset_version : semantic_version.Version, optional
        Specific version of the included batpy dataset, otherwise latest
        version available, by default None.

    Returns
    -------
    str
        File content as string.
    """
    data_dir = "data/"
    if isinstance(dataset_version, str):
        if dataset_version == "":
            dataset_version = None
        else:
            dataset_version = semantic_version.Version(dataset_version)

    if dataset_version is None:
        dataset_version = get_latest_batpy_dataset_version()

    if dataset_version:
        data_dir = (
            data_dir
            + str(dataset_version.major)
            + "."
            + str(dataset_version.minor)
            + "."
            + str(dataset_version.patch)
            + "/"
        )

    if not dataset_name.endswith(".toml"):
        dataset_name += ".toml"
    filename = dataset_name

    return get_data(__name__, data_dir + filename).decode()


def get_latest_batpy_dataset_version() -> semantic_version.Version:
    """Get latest batpy dataset version

    Returns
    -------
    semantic_version.Version
        Latest batpy dataset version available
    """
    return max(get_available_batpy_dataset_versions())


def get_available_batpy_dataset_versions() -> list[semantic_version.Version]:
    """Get available batpy dataset versions

    Returns
    -------
    list[semantic_version.Version]
        List of available batpy dataset versions
    """
    # __versions__ =
    # [f.name for f in os.scandir(f"{data.__path__[0]}") if f.is_dir()]
    # __versions__ = [f.name for f in os.scandir("./data/") if f.is_dir()]
    available_versions = []
    for version_dir in data.__versions__:
        try:
            available_versions.append(semantic_version.Version(version_dir))
        except ValueError:
            continue
    return available_versions


def get_available_batpy_dataset_names(
    dataset_version: semantic_version.Version | str = None,
) -> list[str]:
    """Get available batpy dataset names

    Parameters
    ----------
    dataset_version : semantic_version.Version | str, optional
        Specific version of the included batpy dataset, otherwise latest
        version available, by default None.

    Returns
    -------
    list[str]
        List of included batpy dataset names.

    Raises
    ------
    ValueError
        If 'dataset_version' is not available.
    """
    # import data

    batpy_dataset_names = []
    data_dir = data.__path__[0] + "/"

    if isinstance(dataset_version, str):
        if dataset_version == "":
            dataset_version = None
        else:
            dataset_version = semantic_version.Version(dataset_version)

    if dataset_version is None:
        dataset_version = get_latest_batpy_dataset_version()

    if dataset_version:
        data_dir = (
            data_dir
            + str(dataset_version.major)
            + "."
            + str(dataset_version.minor)
            + "."
            + str(dataset_version.patch)
            + "/"
        )

    print(data_dir)

    if dataset_version in get_available_batpy_dataset_versions():
        batpy_dataset_names = next(os.walk(data_dir), (None, None, []))[
            2
        ]  # [] if no file
    else:
        raise ValueError(f"dataset version {dataset_version} is not available")

    return batpy_dataset_names


# def main():
#     """main"""
#     print(get_available_batpy_dataset_versions())
#     print(get_latest_batpy_dataset_version())
#     print(get_available_batpy_dataset_names("0.0.0"))


# if __name__ == "__main__":
#     main()
