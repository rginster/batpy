# -*- coding: UTF-8 -*-
"""Module, which connects batpac and brightway
"""

from pathlib import Path

from batpy.batpac_battery import BatpacBattery
from batpy.batpac_tool import BatpacTool
from batpy.batpy_workbook import BatpyWorkbook
from batpy.formula_engine import evaluate_formula


class BrightwayConnector(BatpyWorkbook):
    """Connector for interaction with BatPaC and brightway2

    This class is used to connect BatPaC with brightway2.
    """

    def __init__(
        self,
        brightway_workbook_path: Path,
        workbook_visible: bool = False,
    ) -> None:
        """Initialize brightway2

        Initialize the brightway2 workbook object.

        Parameters
        ----------
        brightway_workbook_path : Path
            Path to the brightway2 workbook file (*.xlsx).
        workbook_visible : bool, optional
            True, if workbook should be visible during operation, by default
            False.
        """
        super().__init__(brightway_workbook_path, workbook_visible)
        self._chunk_length = 3

    def load_batpac_to_brightway_configuration(
        self, path_batpac_to_brightway_file: Path | str
    ) -> None:
        """Load user file configuration

        Loads a single configuration from a TOML file, string or dictionary.

        Parameters
        ----------
        path_to_user_file : Path | str
            Path to the TOML configuration file or configuration as string.
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
