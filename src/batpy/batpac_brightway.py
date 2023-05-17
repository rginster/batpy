# -*- coding: UTF-8 -*-
"""Module, which connects batpac and brightway
"""
import logging
from pathlib import Path

import semantic_version
import xlwings as xw

import batpy
from batpy.batpac_battery import BatpacBattery
from batpy.batpac_tool import BatpacTool
from batpy.batpac_util import load_configuration
from batpy.formula_engine import evaluate_formula
from batpy.is_version_compatible import is_version_compatible


class BrightwayConnector:
    """Connector for interaction with BatPaC and brightway2

    This class is used to connect BatPaC with brightway2.
    """

    def __init__(
        self,
        brightway_workbook_path: Path,
        excel_visible: bool = False,
    ) -> None:
        """Initialize brightway2

        Initialize the brightway2 workbook object.

        Parameters
        ----------
        brightway_workbook_path : Path
            Path to the brightway2 Excel file (*.xlsx).
        excel_visible : bool, optional
            True, if Excel should be visible during operation, by default
            False.
        """
        logging.info("[ ] Create brigthway2 from %s", brightway_workbook_path)
        self.version = semantic_version.Version(batpy.__version__)
        self.workbook = xw.Book(brightway_workbook_path)
        self.workbook.app.visible = excel_visible
        self._chunk_length = 3
        self.properties = {}
        logging.info("[+] Created brightway2 from %s", brightway_workbook_path)

    def __del__(self) -> None:
        """Destructor of brightway2 workbook object

        Set the Excel calculation method to "automatic" and the
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
        self, path_to_user_file: Path | str | dict
    ) -> dict:
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
        config = load_configuration(path_to_user_file)
        config_metadata = config.pop("batpy")
        self.is_version_compatible(
            semantic_version.Version(config_metadata["BatPaC SemVer"])
        )
        return config

    def load_batpac_to_brightway_configuration(
        self, path_batpac_to_brightway_file: Path | str | dict
    ) -> None:
        """Load user file configuration

        Loads a single configuration from a TOML file, string or dictionary.

        Parameters
        ----------
        path_to_user_file : Path | str | dict
            Path to the TOML configuration file or configuration as string or
            dictionary.
        """
        self.properties = self._load_user_configuration(
            path_batpac_to_brightway_file
        )

    def _check_data_chunk(
        self,
        chunk_to_check: list,
        batpac: BatpacTool,
        battery: BatpacBattery,
        batpac_config: Path | str | dict,
    ) -> list:
        """Checks data from list of chunks

        Converts the references of the list and combines the single chunks into
        a list of strings.

        Parameters
        ----------
        chunk_to_check : list
            List of chunks to check
        batpac : BatpacTool
            Batpac object from which data should be read.
        battery : BatpacBattery
            Battery object from which data should be read.
        batpac_config : Path | str | dict
            Configuration of the BatPaC tool with the corresponding cell ranges

        Returns
        -------
        list
            List of converted strings
        """
        chunk_list = []
        for sublist_in_chunk in chunk_to_check:
            if sublist_in_chunk[0] == "":
                chunk_list.append(str(sublist_in_chunk[1]))
            else:
                chunk_list.append(
                    str(
                        batpac.read_value_battery(
                            sublist_in_chunk[0],
                            sublist_in_chunk[1],
                            battery,
                            batpac_config,
                        )
                    )
                )
            if len(sublist_in_chunk) == self._chunk_length:
                chunk_list.append(
                    str(sublist_in_chunk[self._chunk_length - 1])
                )
        return chunk_list

    def _get_data_from_chunk(
        self,
        chunk_to_write: list,
        batpac: BatpacTool,
        battery: BatpacBattery,
        batpac_config: Path | str | dict,
    ) -> float:
        """Get data from chunk

        Converts the chunks into a float.

        Parameters
        ----------
        chunk_to_write : list
            List of chunks to write
        batpac : BatpacTool
            Batpac object from which data should be read.
        battery : BatpacBattery
            Battery object from which data should be read.
        batpac_config : Path | str | dict
            Configuration of the BatPaC tool with the corresponding cell ranges

        Returns
        -------
        float
            Calculated float of the chunk
        """
        data_chunk = self._check_data_chunk(
            chunk_to_write, batpac, battery, batpac_config
        )
        formula = "".join(data_chunk)
        return evaluate_formula(formula)

    def _write_value_direct(
        self, worksheet: str, cell_range: str, value: any
    ) -> None:
        """Write value in brightway Excel tool

        Write a value directly in the brightway Excel tool.

        Parameters
        ----------
        worksheet : str
            Name of the brightway Excel tool worksheet.
        cell_range : str
            Cell range of the brightway Excel tool.
        value : any
            Value to write in the brightway Excel tool.
        """
        self.workbook.sheets[worksheet][cell_range].value = value

    def export_batpac_battery_to_brightway(
        self,
        batpac: BatpacTool,
        battery: BatpacBattery,
        batpac_config: Path | str | dict,
    ) -> None:
        """Export battery from BatPaC in brightway worksheet

        Export specified battery from BatPaC Excel tool in the brightway2 Excel
        worksheet.

        Parameters
        ----------
        batpac : BatpacTool
            BatPaC object to read from.
        battery : BatpacBattery
            Battery object to export.
        batpac_config : Path | str | dict
            Path to the TOML configuration file or configuration as string or
            dictionary.

        Raises
        ------
        KeyError
            If battery object is not in the specified batpac object.
        """
        if not self.properties:
            raise KeyError(
                "No configuration file. \
Use 'load_batpac_to_brightway_configuration'."
            )
        if battery not in batpac.batteries:
            raise KeyError("Battery not in BatPaC object.")
        self.stop_automatic_calculation()

        for (
            brightway_sheet_name,
            brightway_sheet_item,
        ) in self.properties.items():
            for (
                brightway_sheet_item_key,
                brightway_sheet_item_value,
            ) in brightway_sheet_item.items():
                chunks = [
                    brightway_sheet_item_value[1][
                        x : x + self._chunk_length  # noqa: E203
                    ]
                    for x in range(
                        0,
                        len(brightway_sheet_item_value[1]),
                        self._chunk_length,
                    )
                ]
                self._write_value_direct(
                    brightway_sheet_name,
                    brightway_sheet_item_value[0][0],
                    self._get_data_from_chunk(
                        chunks, batpac, battery, batpac_config
                    ),
                )
                del brightway_sheet_item_key
        self.start_automatic_calculation()

    def _read_value_direct(self, worksheet: str, cell_range: str) -> any:
        """Read value from brightway Excel tool

        Read a value directly from the brightway Excel tool.

        Parameters
        ----------
        worksheet : str
            Name of the brightway Excel tool worksheet.
        cell_range : str
            Cell range of the brightway Excel tool.

        Returns
        -------
        any
            Value of the brightway Excel tool cell.

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

    def stop_automatic_calculation(self) -> None:
        """Stop automatic Excel calculation
        Stop the automatic Excel and BatPaC calculation.
        """
        self.workbook.app.calculation = "manual"
        self.workbook.app.screen_updating = False

    def start_automatic_calculation(self) -> None:
        """Start automatic Excel calculation
        Start the automatic Excel and BatPaC calculation.
        """
        self.workbook.app.calculation = "automatic"
        self.workbook.app.screen_updating = True

    def save(self, path: Path = None) -> None:
        """Save brightway Excel tool

        Save the brightway Excel tool or save the brightway Excel tool in
        another path.

        Parameters
        ----------
        path : Path, optional
            If the path is specified, the brightway Excel tool will be saved
            under the path, by default None will overwrite the current
            brightway Excel tool.
        """
        logging.info("[ ] Save workbook")
        self.workbook.save(path)
        self.workbook = xw.Book(path)
        logging.info("[+] Saved workbook in %s", path)

    def close(self) -> bool:
        """Close brightway Excel tool

        Close the brightway Excel tool if other workbooks are open, otherwise
        the Excel instance will be closed.

        Returns
        -------
        bool
            True, if brightway Excel tool is closed.
        """
        if len(self.workbook.app.books) == 1:
            self.workbook.app.quit()
            logging.info("[+] Workbook and Excel closed")
            return True
        self.workbook.close()
        logging.info("[+] Workbook closed")
        return True
