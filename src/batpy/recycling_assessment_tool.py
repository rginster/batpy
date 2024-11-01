# -*- coding: UTF-8 -*-
"""Module, which connects batpac and brightway2 with the recycling assessment
tool (RAT).
"""
import logging
from pathlib import Path

from batpy.batpac_battery import BatpacBattery
from batpy.batpac_tool import BatpacTool
from batpy.batpy_workbook import BatpyWorkbook
from batpy.brightway import BrightwayConnector
from batpy.formula_engine import evaluate_formula


class RATConnector(BatpyWorkbook):
    """Connector for interaction with BatPaC and brightway2 with the Recycling
    Assessment Tool (RAT).

    This class is used to connect BatPaC and brightway2 with RAT.
    """

    def __init__(
        self,
        rat_workbook_path: Path,
        excel_cell_definitions_toml_path: Path | str,
        workbook_visible: bool = False,
    ) -> None:
        """Initialize RAT

        Initialize the RAT workbook object.

        Parameters
        ----------
        rat_workbook_path : Path
            Path to the RAT workbook file (*.xlsx).
        workbook_visible : bool, optional
            True, if workbook should be visible during operation, by default
            False.
        """
        super().__init__(rat_workbook_path, workbook_visible)
        self.excel_cells = self._load_user_configuration(
            excel_cell_definitions_toml_path
        )
        self._chunk_length = 3
        self.properties_batpac = None
        self.properties_brightway = None

    def load_batpac_to_rat_configuration(
        self, path_batpac_to_rat_file: Path | str
    ) -> None:
        """Load user file configuration

        Loads a single configuration from a TOML file, string or dictionary.

        Parameters
        ----------
        path_to_user_file : Path | str
            Path to the TOML configuration file or configuration as string.
        """
        self.properties_batpac = self._load_user_configuration(
            path_batpac_to_rat_file
        )

    def load_rat_to_brightway_configuration(
        self, path_rat_to_brightway_file: Path | str
    ) -> None:
        """Load user file configuration

        Loads a single configuration from a TOML file, string or dictionary.

        Parameters
        ----------
        path_to_user_file : Path | str
            Path to the TOML configuration file or configuration as string.
        """
        self.properties_brightway = self._load_user_configuration(
            path_rat_to_brightway_file
        )

    def _wb_helper_range(
        self,
        worksheet: str,
        name: str,
        additional_cell_config: Path | dict | str = None,
    ) -> str:
        """Helper function for workbook range

        Function to find the cell range of a specified cell description.

        Parameters
        ----------
        worksheet : str
            Name of the rat Excel tool worksheet.
        name : str
            Name of the rat Excel cell description.
        additional_cell_config : Path | dict | str, optional
            Path to TOML file or dictionary or str (default dataset), which
            contains additional cell configuration to consider,
            by default None.

        Returns
        -------
        str
            Excel cell range.

        Raises
        ------
        KeyError
            Raises KeyError, if worksheet name or cell description could not be
            found.
        """
        try:
            if additional_cell_config is not None:
                if isinstance(additional_cell_config, dict):
                    range_dict = additional_cell_config
                else:
                    range_dict = self._load_user_configuration(
                        additional_cell_config
                    )
            else:
                range_dict = self.excel_cells

            cell_range = range_dict[worksheet][name]
            return cell_range

        except BaseException as error:
            logging.error("An exception occurred: %s", error)
            logging.warning("[!] Key %s , %s not found", worksheet, name)
            raise KeyError from error

    def read_value(
        self,
        worksheet: str,
        name: str,
        additional_cell_config: Path | dict | str = None,
    ) -> any:
        """Read value from rat Excel tool

        Read value from rat Excel tool without input the exact cell range.

        Parameters
        ----------
        worksheet : str
            Name of the rat Excel tool worksheet.
        name : str
            Name of the rat Excel cell description.
        additional_cell_config : Path | dict | str, optional
            Path to TOML file or dictionary or string (default dataset), which
            contains additional cell configuration to consider,
            by default None.

        Returns
        -------
        any
            Value of the rat Excel tool cell.
        """
        return self._read_value_direct(
            worksheet,
            self._wb_helper_range(worksheet, name, additional_cell_config),
        )

    def _check_data_chunk_batpac(
        self,
        chunk_to_check: list,
        batpac: BatpacTool,
        battery: BatpacBattery,
        batpac_config: Path | str | dict,
    ) -> list:
        """Checks data from list of chunks from batpac

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
                        batpac.read_value(
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

    def _get_data_from_chunk_batpac(
        self,
        chunk_to_write: list,
        batpac: BatpacTool,
        battery: BatpacBattery,
        batpac_config: Path | str | dict,
    ) -> float:
        """Get data from chunk from batpac

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
        data_chunk = self._check_data_chunk_batpac(
            chunk_to_write, batpac, battery, batpac_config
        )
        formula = "".join(data_chunk)
        return evaluate_formula(formula)

    def _check_data_chunk(
        self,
        chunk_to_check: list,
        rat_config: Path | str | dict,
    ) -> list:
        """Checks data from list of chunks

        Converts the references of the list and combines the single chunks into
        a list of strings.

        Parameters
        ----------
        chunk_to_check : list
            List of chunks to check
        rat_config : Path | str | dict
            Configuration of the rat tool with the corresponding cell ranges

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
                        self.read_value(
                            sublist_in_chunk[0],
                            sublist_in_chunk[1],
                            rat_config,
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
        rat_config: Path | str | dict,
    ) -> float:
        """Get data from chunk

        Converts the chunks into a float.

        Parameters
        ----------
        chunk_to_write : list
            List of chunks to write
        rat_config : Path | str | dict
            Configuration of the rat tool with the corresponding cell ranges

        Returns
        -------
        float
            Calculated float of the chunk
        """
        data_chunk = self._check_data_chunk(chunk_to_write, rat_config)
        formula = "".join(data_chunk)
        return evaluate_formula(formula)

    def export_batpac_battery_to_rat(
        self,
        batpac: BatpacTool,
        battery: BatpacBattery,
        batpac_config: Path | str | dict,
    ) -> None:
        """Export battery from BatPaC in rat worksheet

        Export specified battery from BatPaC Excel tool in the RAT Excel
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
        if not self.properties_batpac:
            raise KeyError(
                "No configuration file. \
Use 'load_batpac_to_rat_configuration'."
            )
        if battery not in batpac.batteries:
            raise KeyError("Battery not in BatPaC object.")
        self.stop_automatic_calculation()

        for (
            rat_sheet_name,
            rat_sheet_item,
        ) in self.properties_batpac.items():
            for (
                rat_sheet_item_key,
                rat_sheet_item_value,
            ) in rat_sheet_item.items():
                chunks = [
                    rat_sheet_item_value[1][
                        x : x + self._chunk_length  # noqa: E203
                    ]
                    for x in range(
                        0,
                        len(rat_sheet_item_value[1]),
                        self._chunk_length,
                    )
                ]
                self._write_value_direct(
                    rat_sheet_name,
                    rat_sheet_item_value[0][0],
                    self._get_data_from_chunk_batpac(
                        chunks, batpac, battery, batpac_config
                    ),
                )
                del rat_sheet_item_key
        self.start_automatic_calculation()

    def export_rat_to_brightway(
        self,
        brightway: BrightwayConnector,
        rat_config: Path | str | dict,
    ) -> None:
        """Export current battery from rat to brightway worksheet

        Export the current battery from the recycling assessment tool to the
        brightway worksheet.

        Parameters
        ----------
        brightway : BrightwayConnector
            Brightway object to export the data.
        rat_config : Path | str | dict
            Path to the TOML configuration file or configuration as string or
            dictionary.

        Raises
        ------
        KeyError
            If no properties are loaded.
        """
        if not self.properties_brightway:
            raise KeyError(
                "No configuration file. \
Use 'load_rat_to_brightway_configuration'."
            )
        self.stop_automatic_calculation()

        for (
            rat_sheet_name,
            rat_sheet_item,
        ) in self.properties_brightway.items():
            for (
                rat_sheet_item_key,
                rat_sheet_item_value,
            ) in rat_sheet_item.items():
                chunks = [
                    rat_sheet_item_value[1][
                        x : x + self._chunk_length  # noqa: E203
                    ]
                    for x in range(
                        0,
                        len(rat_sheet_item_value[1]),
                        self._chunk_length,
                    )
                ]
                # pylint: disable=W0212
                brightway._write_value_direct(
                    rat_sheet_name,
                    rat_sheet_item_value[0][0],
                    self._get_data_from_chunk(chunks, rat_config),
                )
                del rat_sheet_item_key
        self.start_automatic_calculation()
