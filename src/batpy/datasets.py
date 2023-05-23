# -*- coding: UTF-8 -*-
"""Module to load default batpy datasets
"""

# import logging
import os
import shutil
from pathlib import Path
from pkgutil import get_data, get_loader
from types import ModuleType

import semantic_version

from batpy import data, utility_functions


def get_available_batpy_dataset_versions() -> list[semantic_version.Version]:
    """Get available batpy dataset versions

    Returns
    -------
    list[semantic_version.Version]
        List of available batpy dataset versions
    """

    available_versions = []
    for version_dir in data.__versions__:
        try:
            available_versions.append(semantic_version.Version(version_dir))
        except ValueError:
            continue
    return available_versions


def get_latest_batpy_dataset_version() -> semantic_version.Version:
    """Get latest batpy dataset version

    Returns
    -------
    semantic_version.Version
        Latest batpy dataset version available
    """
    return max(get_available_batpy_dataset_versions())


def get_batpy_dataset(
    dataset_name: str, dataset_version: semantic_version.Version | str = None
) -> str:
    """Get included batpy dataset

    Parameters
    ----------
    dataset_name : str
        Name of included batpy dataset.
    dataset_version : semantic_version.Version | str, optional
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

    if dataset_version in get_available_batpy_dataset_versions():
        batpy_dataset_names = next(os.walk(data_dir), (None, None, []))[2]
        batpy_dataset_names = [
            dataset_name
            for dataset_name in batpy_dataset_names
            if dataset_name.endswith(".toml")
        ]

    else:
        raise ValueError(f"dataset version {dataset_version} is not available")

    return batpy_dataset_names


def get_dataset_information(dataset_stream: str) -> str:
    """Get information of dataset

    Parameters
    ----------
    dataset_stream : str
        String representation of dataset.

    Returns
    -------
    str
        Available dataset information

    Raises
    ------
    KeyError
        If no information is specified
    """
    config = utility_functions.load_configuration(dataset_stream)
    try:
        return config["batpy"]["information"]
    except KeyError as error:
        raise KeyError("Information for dataset are not available") from error


def get_available_batpy_datasets(
    dataset_version: semantic_version.Version | str = None,
) -> dict[str, str]:
    """Get available batpy datasets

    Parameters
    ----------
    dataset_version : semantic_version.Version | str, optional
        Specific version of the included batpy dataset, otherwise latest
        version available, by default None.

    Returns
    -------
    dict[str, str]
        Returns available batpy dataset names and their corresponding
        information.
    """
    dataset_names = get_available_batpy_dataset_names(dataset_version)
    dataset_names_information = {
        name: get_dataset_information(get_batpy_dataset(name))
        for name in dataset_names
    }
    return dataset_names_information


def get_path(module_name: str | ModuleType) -> Path:
    """Get module path

    Parameters
    ----------
    module_name : str | ModuleType
        Module name or class

    Returns
    -------
    Path
        Path of the module
    """
    return Path(get_loader(module_name).get_filename()).parent


def copy_integrated_brightway_workbook(path_to_save_workbook: Path) -> None:
    """Copy integrated brightway2 workbook to specified location

    Parameters
    ----------
    path_to_save_workbook : Path
        Path to save integrated brigthway2 workbook
    """
    brightway2_workbook = Path(
        get_path(data) / "excel_workbooks" / "BatPaC-Brightway.xlsx"
    )
    excel_workbook_destination = Path(path_to_save_workbook)
    shutil.copy(brightway2_workbook, excel_workbook_destination)


def copy_integrated_dataset(
    dataset_to_export: str,
    path_to_save_toml_file: Path,
    dataset_version_to_export: semantic_version.Version | str = None,
) -> None:
    """Copy integrated dataset to specified location

    Parameters
    ----------
    dataset_to_export : str
        Name of the dataset to export
    path_to_save_toml_file : Path
        Path to save integrated dataset
    dataset_version_to_export : semantic_version.Version | str, optional
        Specific version of the included batpy dataset, otherwise latest
        version available, by default None.
    """
    if isinstance(dataset_version_to_export, str):
        if dataset_version_to_export == "":
            dataset_version_to_export = None
        else:
            dataset_version_to_export = semantic_version.Version(
                dataset_version_to_export
            )

    if dataset_version_to_export is None:
        dataset_version_to_export = get_latest_batpy_dataset_version()

    if dataset_version_to_export:
        data_dir = (
            str(dataset_version_to_export.major)
            + "."
            + str(dataset_version_to_export.minor)
            + "."
            + str(dataset_version_to_export.patch)
            + "/"
        )
    if not dataset_to_export.endswith(".toml"):
        dataset_to_export += ".toml"

    if dataset_to_export in get_available_batpy_dataset_names(
        dataset_version_to_export
    ):
        dataset_path = Path(get_path(data) / data_dir / dataset_to_export)
        dataset_destination = Path(path_to_save_toml_file)
        shutil.copy(dataset_path, dataset_destination)
    else:
        raise KeyError(f"Dataset {dataset_to_export} is not available.")
