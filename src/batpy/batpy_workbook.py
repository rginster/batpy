# -*- coding: UTF-8 -*-
"""Module, which includes the basic workbook class
"""
import logging
from pathlib import Path

import semantic_version
import xlwings as xw

import batpy
from batpy.utility_functions import is_version_compatible, load_configuration


class BatpyWorkbook:
    """Base class to interact with workbooks"""

    def __init__(
        self,
        batpy_workbook_path: Path,
        workbook_visible: bool = False,
    ) -> None:
        """Initialize batpy workbook

        Initialize the batpy workbook object.

        Parameters
        ----------
        batpy_workbook_path : Path
            Path to the batpy workbook file (*.xlsx | *.xlsm).
        workbook_visible : bool, optional
            True, if workbook should be visible during operation, by default
            False.
        """
        logging.info("[ ] Create workbook from %s", batpy_workbook_path)
        self.version = semantic_version.Version(batpy.__version__)
        self.workbook = xw.Book(batpy_workbook_path)
        self.workbook.app.visible = workbook_visible
        self.properties = {}
        logging.info("[+] Created workbook from %s", batpy_workbook_path)

    def __del__(self) -> None:
        """Destructor of batpy workbook object

        Set the workbook calculation method to "automatic" and the
        "screen_updating" to True after object destruction.
        """
        try:
            self.workbook.app.calculation = "automatic"
            self.workbook.app.screen_updating = True
        except BaseException as error:
            logging.error("An exception occurred: %s", error)
            raise KeyError(
                "Could not access the workbook (may already be closed)."
            ) from error

    def save(self, path: Path = None) -> None:
        """Save batpy workbook

        Save the batpy workbook or save the batpy workbook in another path.

        Parameters
        ----------
        path : Path, optional
            If the path is specified, the batpy workbook will be saved
            under the path, by default None will overwrite the current
            batpy workbook.
        """
        logging.info("[ ] Save workbook")
        self.workbook.save(path)
        if path:
            self.workbook = xw.Book(path)
        logging.info("[+] Saved workbook in %s", path)

    def close(self) -> bool:
        """Close batpy workbook

        Close the batpy workbook if other workbooks are open, otherwise
        the Excel instance will be closed.

        Returns
        -------
        bool
            True, if batpy workbook is closed.
        """
        if len(self.workbook.app.books) == 1:
            self.workbook.app.quit()
            logging.info("[+] Workbook and Excel closed")
            return True
        self.workbook.close()
        logging.info("[+] Workbook closed")
        return True

    def stop_automatic_calculation(self) -> None:
        """Stop automatic Excel calculation"""
        self.workbook.app.calculation = "manual"
        self.workbook.app.screen_updating = False

    def start_automatic_calculation(self) -> None:
        """Start automatic Excel calculation"""
        self.workbook.app.calculation = "automatic"
        self.workbook.app.screen_updating = True

    def is_version_compatible(
        self,
        version_to_check: semantic_version.Version,
        include_minor: bool = False,
    ) -> bool:
        """Check for version compatibility

        Check if two versions (major.minor.patch) are compatible. Thereby a
        version is compatible if major is equal. If minor should also be
        included a version is compatible if major is equal and minor is greater
        or equal.

        Parameters
        ----------
        version_to_check : semantic_version.Version
            Version to be checked against self.version.
        include_minor : bool, optional
            Check if minor version of version_to_check is greater or equal to
            self.version's minor, by default False.

        Returns
        -------
        bool
            True, if version is compatible.

        Raises
        ------
        ValueError
            If version is not compatible a ValueError will occur.
        """
        return is_version_compatible(
            self.version, version_to_check, include_minor
        )

    def _load_user_configuration(
        self, path_to_configuration: Path | str
    ) -> dict:
        """Load configuration

        Loads a single configuration from a TOML file or string.

        Parameters
        ----------
        path_to_configuration : Path | str
            Path to the TOML configuration file or configuration as string.

        Returns
        -------
        dict
            Returns dictionary representation of configuration.
        """
        config = load_configuration(path_to_configuration)
        config_metadata = config.pop("batpy")
        self.is_version_compatible(
            semantic_version.Version(config_metadata["BatPaC SemVer"])
        )
        return config

    def _write_value_direct(
        self, worksheet: str, cell_range: str, value: any
    ) -> None:
        """Write value in batpy workbook

        Write a value directly in the batpy workbook.

        Parameters
        ----------
        worksheet : str
            Name of the batpy workbook worksheet.
        cell_range : str
            Cell range of the batpy workbook.
        value : any
            Value to write in the batpy workbook.
        """
        self.workbook.sheets[worksheet][cell_range].value = value

    def _read_value_direct(self, worksheet: str, cell_range: str) -> any:
        """Read value from batpy workbook

        Read a value directly from the batpy workbook.

        Parameters
        ----------
        worksheet : str
            Name of the batpy workbook worksheet.
        cell_range : str
            Cell range of the batpy workbook.

        Returns
        -------
        any
            Value of the batpy workbook cell.

        Raises
        ------
        KeyError
            Raises KeyError if the specified worksheet or range could not be
            found.
        """
        try:
            value = self.workbook.sheets[worksheet][cell_range].value
            return value
        except BaseException as error:
            logging.error("An exception occurred: %s", error)
            logging.warning("[!] Key %s , %s not found", worksheet, cell_range)
            raise KeyError from error
