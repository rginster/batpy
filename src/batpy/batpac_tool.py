# -*- coding: UTF-8 -*-
"""Module, which includes the class BatpacTool
"""
import logging
from pathlib import Path

import semantic_version
import toml
import xlwings as xw
from prettytable import PrettyTable
from tqdm import tqdm

import batpy
from batpy.batpac_battery import BatpacBattery
from batpy.utility_functions import is_version_compatible, load_configuration


class BatpacTool:
    """BatPaC class which interacts with the BatPaC Excel tool

    This BatPaC class is used to interact directly with the BatPaC Excel tool
    and can store individual batteries (class BatPaC_battery) and additional
    parameters of the BatPaC Excel tool in the dictionary properties.
    """

    def _load_user_file(self, path_to_user_file: Path | str) -> dict:
        """Load user file configuration

        Load the user configuration from a TOML user file.

        Parameters
        ----------
        path_to_user_file : Path | str
            Path to the TOML user file or configuration as string.

        Returns
        -------
        dict
            Returns dictionary representation of read TOML file.
        """
        config = load_configuration(path_to_user_file)
        config_metadata = config.pop("batpy")
        self.is_version_compatible(
            semantic_version.Version(config_metadata["BatPaC SemVer"])
        )
        return config

    def __init__(
        self,
        batpac_workbook_path: Path,
        cell_definition_user_input_toml_path: Path | str,
        cell_definition_calculation_validation_results: Path | str = None,
        # cell_definition_additional_user_input_toml_path: Path = None,
        # cell_definition_additional_user_results_toml_path: Path = None,
        excel_visible: bool = False,
    ) -> None:
        """Initialize BatPaC

        Initialize the BatPaC object.

        Parameters
        ----------
        batpac_workbook_path : Path
            Path to the BatPaC Excel tool (*.xlsm).
        cell_definition_user_input_toml_path : Path | str
            Path to the TOML file or string (default dataset), which contains
            the configuration for the standard user input cells (defined by
            Argonne National Laboratory) in the BatPaC Excel tool.
        cell_definition_calculation_validation_results : Path | str, optional
            Path to the TOML file or string (default dataset), which contains
            the configuration for the calculation and validation results in the
            BatPaC Excel tool, by default None.
        cell_definition_additional_user_input_toml_path : Path, optional
            Path to the TOML file, which contains additional cells for user
            input, that are not included in the standard user inputs in the
            BatPaC Excel tool, by default None.
        cell_definition_additional_user_results_toml_path : Path, optional
            Path to the TOML file, which contains additional cells for  user
            input, that are not included in the standard user inputs in the
            BatPaC Excel tool, by default None.
        excel_visible : bool, optional
            True, if Excel should be visible during operation, by default
            False.
        """
        logging.info(
            "[ ] Create BatPaC from %s and load cell references from %s",
            batpac_workbook_path,
            cell_definition_user_input_toml_path,
        )
        self.version = semantic_version.Version(batpy.__version__)

        self.excel_cells = self._load_user_file(
            cell_definition_user_input_toml_path
        )
        if cell_definition_calculation_validation_results:
            self.toml_calculation_validation_results = self._load_user_file(
                cell_definition_calculation_validation_results
            )
        self.batteries = []
        self.workbook = xw.Book(batpac_workbook_path)
        # self.app = self.workbook.app
        self.workbook.app.visible = excel_visible
        self.max_batteries = 7
        self.properties = {}
        logging.info(
            "[+] Created BatPaC from %s and load \
                    cell references from %s",
            batpac_workbook_path,
            cell_definition_user_input_toml_path,
        )

    def __del__(self) -> None:
        """Destructor of BatPac object

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

    def load_batpac_file(self, path_to_batpac_file: Path | str) -> None:
        """Load BatPaC configuration

        Load the properties for the BatPaC object from a TOML battery
        configuration file.

        Parameters
        ----------
        path_to_batpac_file : Path | str
            Path to the TOML BatPaC configuration file.
        """
        logging.info("[ ] Load BatPaC file from %s", path_to_batpac_file)

        try:
            Path.exists(Path(path_to_batpac_file))
            config = toml.load(path_to_batpac_file)
        except (AttributeError, OSError):
            config = toml.loads(path_to_batpac_file)
        config_metadata = config.pop("batpy")
        if self.is_version_compatible(
            semantic_version.Version(config_metadata["BatPaC SemVer"])
        ):
            self.properties = config
            logging.info("[+] Loaded BatPaC file from %s", path_to_batpac_file)
            logging.debug("[ ] BatPaC properties %s", self.properties)

    def add_battery(self, batteries: list[BatpacBattery]) -> None:
        """Add battery object to BatPaC object

        Add multiple battery objects to the BatPaC object.

        Parameters
        ----------
        batteries : list[BatPaC_battery]
            List of BatPaC_battery objects to include in the BatPaC object.
        """
        for battery in batteries:
            if len(self.batteries) + 1 <= self.max_batteries:
                self.batteries.append(battery)
            else:
                print(
                    f"Battery {battery.name} ({battery}) exceeds the limit of \
                        batteries for a single workbook"
                )
                logging.warning(
                    "[!] Battery %s (%s) exceeds the limit of batteries for a \
                        single workbook",
                    battery.name,
                    battery,
                )

    def set_new_property(self, sheet: str, name: str, value: any) -> None:
        """Set a new property of the battery

        Set an existing property of the BatPaC tool or create a new one in the
        format {"sheet" : {"name" : value} }.

        Parameters
        ----------
        sheet : str
            Name of the BatPaC Excel sheet.
        name : str
            Name of the BatPaC Excel cell description.
        value : any
            Value of the BatPaC Excel cell.
        """
        try:
            self.properties[sheet][name] = value
        except KeyError:
            self.properties.update({sheet: {name: value}})

    def load_batteries_file(
        self, path_to_batteries_file: Path, batteries: list[BatpacBattery]
    ) -> None:
        """Load batteries configuration

        Load the configuration for the batteries from TOML configuration file
        and add these batteries to the BatPaC object.
        Beware: This will clear all previous assigned batteries of the BatPaC
        object!

        Parameters
        ----------
        path_to_batteries_file : Path
            Path to the TOML batteries configuration file.
        batteries : list[BatPaC_battery]
            List of BatPaC_battery objects to load battery properties from file
            and add to BatPaC object.
        """
        logging.info("[ ] Load batteries from file %s", path_to_batteries_file)
        self.batteries.clear()
        self.add_battery(batteries)
        for battery in self.batteries:
            battery.load_battery_file(path_to_batteries_file, battery.name)
            logging.debug(
                "[ ] Battery %s properties %s",
                battery.name,
                battery.properties,
            )
        logging.info(
            "[+] Batteries from file %s loaded", path_to_batteries_file
        )

    def _write_value_direct(
        self, worksheet: str, cell_range: str, value: any
    ) -> None:
        """Write value in BatPaC Excel tool

        Write a value directly in the BatPaC Excel tool.

        Parameters
        ----------
        worksheet : str
            Name of the BatPaC Excel tool worksheet.
        cell_range : str
            Cell range of the BatPaC Excel tool.
        value : any
            Value to write in the BatPaC Excel tool.
        """
        self.workbook.sheets[worksheet][cell_range].value = value

    def _read_value_direct(self, worksheet: str, cell_range: str) -> any:
        """Read value from BatPaC Excel tool

        Read a value directly from the BatPaC Excel tool.

        Parameters
        ----------
        worksheet : str
            Name of the BatPaC Excel tool worksheet.
        cell_range : str
            Cell range of the BatPaC Excel tool.

        Returns
        -------
        any
            Value of the BatPaC Excel tool cell.

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

    def _wb_helper_range(
        self,
        worksheet: str,
        name: str,
        battery: BatpacBattery = None,
        additional_cell_config: Path | dict | str = None,
    ) -> str:
        """Helper function for workbook range

        Function to find the cell range of a specified cell description.

        Parameters
        ----------
        worksheet : str
            Name of the BatPaC Excel tool worksheet.
        name : str
            Name of the BatPaC Excel cell description.
        battery : BatPaC_battery, optional
            BatPaC_battery object, if the returned cell is battery specific, by
            default None.
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
                    range_dict = self._load_user_file(additional_cell_config)
            else:
                range_dict = self.excel_cells

            if battery is None:
                cell_range = range_dict[worksheet][name]
            else:
                cell_range = range_dict[worksheet][
                    "Battery " + str(self.batteries.index(battery) + 1)
                ][name]
            return cell_range
        except BaseException as error:
            logging.error("An exception occurred: %s", error)
            logging.warning("[!] Key %s , %s not found", worksheet, name)
            raise KeyError from error

    def write_value(self, worksheet: str, name: str, value: any) -> None:
        """Write value in BatPaC Excel tool

        Write value in BatPaC Excel tool without input the exact cell range.

        Parameters
        ----------
        worksheet : str
            Name of the BatPaC Excel tool worksheet.
        name : str
            Name of the BatPaC Excel cell description.
        value : any
            Value to write in the BatPaC Excel tool.
        """
        self._write_value_direct(
            worksheet, self._wb_helper_range(worksheet, name), value
        )
        logging.debug(
            "[ ] Write in %s %s (%s) = %s",
            worksheet,
            self._wb_helper_range(worksheet, name),
            name,
            value,
        )

    def read_value(
        self,
        worksheet: str,
        name: str,
        additional_cell_config: Path | dict | str = None,
    ) -> any:
        """Read value from BatPaC Excel tool

        Read value from BatPaC Excel tool without input the exact cell range.

        Parameters
        ----------
        worksheet : str
            Name of the BatPaC Excel tool worksheet.
        name : str
            Name of the BatPaC Excel cell description.
        additional_cell_config : Path | dict | str, optional
            Path to TOML file or dictionary or string (default dataset), which
            contains additional cell configuration to consider,
            by default None.

        Returns
        -------
        any
            Value of the BatPaC Excel tool cell.
        """
        return self._read_value_direct(
            worksheet,
            self._wb_helper_range(
                worksheet,
                name,
                battery=None,
                additional_cell_config=additional_cell_config,
            ),
        )

    def read_value_battery(
        self,
        worksheet: str,
        name: str,
        battery: BatpacBattery,
        additional_cell_config: Path | dict | str = None,
    ) -> any:
        """Read battery specific value from BatPaC Excel tool

        Read battery specific value from BatPaC Excel tool without input the
        exact cell range.

        Parameters
        ----------
        worksheet : str
            Name of the BatPaC Excel tool worksheet.
        name : str
            Name of the BatPaC Excel cell description.
        battery : BatPaC_battery
            BatPaC_battery object, if the returned cell is battery specific, by
            default None.
        additional_cell_config : Path | dict, optional
            Path to TOML file or dictionary or string (default dataset), which
            contains additional cell configuration to consider,
            by default None.

        Returns
        -------
        any
            Value of the BatPaC Excel tool cell.
        """
        return self._read_value_direct(
            worksheet,
            self._wb_helper_range(
                worksheet, name, battery, additional_cell_config
            ),
        )

    def write_value_battery(
        self, worksheet: str, name: str, battery: BatpacBattery, value: any
    ) -> None:
        """Write specific battery value in BatPaC Excel tool

        Write a speicif battery value in the BatPaC Excel tool without input
        the exact cell range.

        Parameters
        ----------
        worksheet : str
            Name of the BatPaC Excel tool worksheet.
        name : str
            Name of the BatPaC Excel cell description.
        battery : BatPaC_battery
            BatPaC_battery object, if the returned cell is battery specific,
            by default None.
        value : any
            Value to write in the BatPaC Excel tool.
        """
        self._write_value_direct(
            worksheet, self._wb_helper_range(worksheet, name, battery), value
        )
        logging.debug(
            "[ ] Write for %s in %s %s (%s) = %s",
            battery.name,
            worksheet,
            self._wb_helper_range(worksheet, name, battery),
            name,
            value,
        )

    def stop_automatic_calculation(self) -> None:
        """Stop automatic Excel calculation
        Stop the automatic Excel and BatPaC calculation.
        """
        self.write_value("Dashboard", "Restart (0/1)", 0)
        self.workbook.app.calculation = "manual"
        self.workbook.app.screen_updating = False

    def start_automatic_calculation(self) -> None:
        """Start automatic Excel calculation
        Start the automatic Excel and BatPaC calculation.
        """
        reset_macro = self.workbook.macro("Module1.Reset")
        reset_macro()
        self.workbook.app.calculation = "automatic"
        self.workbook.app.screen_updating = True

    def read_from_user_input(self, user_read_file: Path | str) -> dict:
        """Read user specified input from BatPaC Excel tool

        Read additional cell values from BatPaC Excel tool specified by user
        input.

        Parameters
        ----------
        user_read_file : Path | str
            Path to the TOML file or string (default dataset) containing
            additional cell ranges from which values are to be read.

        Returns
        -------
        dict
            Dictionary in the format {"sheet" : {"name" : value} }
        """

        additional_cells = self._load_user_file(user_read_file)
        values_dict = additional_cells
        for sheet_name, sheet_key in additional_cells.items():
            for batpac_key, batpac_cell_range in sheet_key.items():
                if isinstance(batpac_cell_range, dict):
                    for (
                        battery_key,
                        battery_cell_range,
                    ) in batpac_cell_range.items():
                        values_dict[sheet_name][batpac_key][
                            battery_key
                        ] = self._read_value_direct(
                            sheet_name, battery_cell_range
                        )
                else:
                    values_dict[sheet_name][
                        batpac_key
                    ] = self._read_value_direct(sheet_name, batpac_cell_range)

        return values_dict

    def read_calculation_and_validation_results(
        self, toml_file_calculation_validation_results: Path | str = None
    ) -> dict:
        """Read calculation and validation results

        Read the calculation and validation results from the BatPaC Excel tool.

        Parameters
        ----------
        toml_file_calculation_validation_results : Path | str, optional
            Path to the TOML file or string (default dataset), containing the
            specified cell ranges of the calculation and validation results,
            by default None.

        Returns
        -------
        dict
            Returns a dictionary of the calculation and validation results.

        Raises
        ------
        KeyError
            If no configuration for calculation and validation found.
        """

        if toml_file_calculation_validation_results is None:
            if self.toml_calculation_validation_results is None:
                logging.warning(
                    "[!] No toml file for calculation and validation found."
                )
                raise KeyError(
                    "No configuration for calculation and validation found."
                )
        else:
            self.toml_calculation_validation_results = self._load_user_file(
                toml_file_calculation_validation_results
            )

        config_errors = ["Configuration Errors (see table to right)"]
        config_warnings = ["Configuration Warnings (see table  to right)"]
        plant_size = ["Plant Size, GWh"]
        power_to_energy = ["Power-to-energy ratio"]
        adequacy_cooling = ["Adequacy of cooling"]
        cathode_thickness = ["Cathode thickness limited by"]
        table_columns = ["Parameter"]
        for battery in self.batteries:
            config_errors.append(
                self.read_value_battery(
                    "Dashboard",
                    "Configuration Errors (see table to right)",
                    battery,
                    self.toml_calculation_validation_results,
                )
            )
            config_warnings.append(
                self.read_value_battery(
                    "Dashboard",
                    "Configuration Warnings (see table  to right)",
                    battery,
                    self.toml_calculation_validation_results,
                )
            )
            plant_size.append(
                self.read_value_battery(
                    "Dashboard",
                    "Plant Size, GWh",
                    battery,
                    self.toml_calculation_validation_results,
                )
            )
            power_to_energy.append(
                self.read_value_battery(
                    "Dashboard",
                    "Power-to-energy ratio",
                    battery,
                    self.toml_calculation_validation_results,
                )
            )
            adequacy_cooling.append(
                self.read_value_battery(
                    "Dashboard",
                    "Adequacy of cooling",
                    battery,
                    self.toml_calculation_validation_results,
                )
            )
            cathode_thickness.append(
                self.read_value_battery(
                    "Dashboard",
                    "Cathode thickness limited by",
                    battery,
                    self.toml_calculation_validation_results,
                )
            )
            table_columns.append(battery.name)

        table = [
            table_columns,
            config_errors,
            config_warnings,
            plant_size,
            power_to_energy,
            adequacy_cooling,
            cathode_thickness,
        ]
        tab = PrettyTable(table[0])
        tab.align["Parameter"] = "l"
        tab.add_rows(table[1:])
        print(tab)
        dict_table = {
            table_columns[0]: table_columns[1:],
            config_errors[0]: config_errors[1:],
            config_warnings[0]: config_warnings[1:],
            plant_size[0]: plant_size[1:],
            power_to_energy[0]: power_to_energy[1:],
            adequacy_cooling[0]: adequacy_cooling[1:],
            cathode_thickness[0]: cathode_thickness[1:],
        }

        return dict_table

    def calculate(self) -> None:
        """Calculate the batteries in the BatPaC Excel tool

        Read all BatPaC_tool properties and its included [BatPaC_battery]
        properties, write these properties in the BatPaC Excel tool,
        and calculate the batteries in the BatPaC Excel tool.
        """
        logging.info("[ ] Start calculation")
        self.stop_automatic_calculation()
        for sheet in tqdm(
            self.properties, "Processing BatPaC configuration in each sheet"
        ):
            for key, value in self.properties[sheet].items():
                if value is not None:
                    self.write_value(sheet, key, value)

        sheets = set()
        for battery in self.batteries:
            sheets.update(battery.properties.keys())

        logging.debug(
            "[ ] Sheets type is %s and sheets available: %s",
            type(sheets),
            sheets,
        )

        for sheet in tqdm(
            sheets, "Processing battery configuration in each sheet"
        ):
            sheet_buffer = {}
            for i, battery in enumerate(self.batteries):
                if sheet in battery.properties:
                    for key, value in battery.properties[sheet].items():
                        if key not in sheet_buffer:
                            sheet_buffer[key] = [None] * self.max_batteries
                        sheet_buffer[key][i] = value
            for key, value in sheet_buffer.items():
                self.write_value_battery(sheet, key, self.batteries[0], value)

        self.start_automatic_calculation()
        logging.info("[+] Finished calculation")

    def save(self, path: Path = None) -> None:
        """Save BatPaC Excel tool

        Save the BatPaC Excel tool or save the BatPaC Excel tool in another
        path.

        Parameters
        ----------
        path : Path, optional
            If the path is specified, the BatPaC Excel tool will be saved under
            the path, by default None will overwrite the current BatPaC Excel
            tool.
        """
        logging.info("[ ] Save workbook")
        self.workbook.save(path)
        self.workbook = xw.Book(path)
        # self.app = self.workbook.app
        logging.info("[+] Saved workbook in %s", path)

    def close(self) -> bool:
        """Close BatPaC Excel tool

        Close the BatPaC Excel tool if other workbooks are open, otherwise the
        Excel instance will be closed.

        Returns
        -------
        bool
            True, if BatPaC Excel tool is closed.
        """
        if len(self.workbook.app.books) == 1:
            self.workbook.app.quit()
            logging.info("[+] Workbook and Excel closed")
            return True
        self.workbook.close()
        logging.info("[+] Workbook closed")
        return True

    def _save_batpac_config(self, batpac_path: Path = None) -> None:
        """Save BatPaC_tool configuration

        Read all BatPaC_tool properties from the BatPaC Excel tool, save
        these properties in the BatPaC_tool object, and write them as TOML
        file.

        Parameters
        ----------
        batpac_path : Path, optional
            If specified, storage path to the TOML file for BatPaC_tool
            properties, by default None.
        """
        for sheet in self.excel_cells:
            for key, value in self.excel_cells[sheet].items():
                if isinstance(value, dict):
                    continue
                self.set_new_property(sheet, key, self.read_value(sheet, key))

        if batpac_path is not None:
            with open(batpac_path, "w", encoding="utf-8") as toml_file:
                for sheet in tqdm(
                    self.properties, "Saving BatPaC config from each sheet"
                ):
                    toml_file.write(f'["{sheet}"]\n')
                    for key, value in self.properties[sheet].items():
                        if value is None or key == "Restart (0/1)":
                            toml_file.write("# ")
                        if isinstance(value, str):
                            toml_file.write(f"'{key}' = '{value}'\n")
                        else:
                            toml_file.write(f"'{key}' = {value}\n")
                    toml_file.write("\n")

    def _save_battery_config(self, battery_path: Path = None) -> None:
        """Save [BatPaC_battery] configuration

        Read all BatPaC_tool included [BatPaC_battery] properties from the
        BatPaC Excel tool, save these properties in the [BatPaC_battery]
        objects, and write them as TOML file.

        Parameters
        ----------
        battery_path : Path, optional
            If specified, storage path to the TOML file for [BatPaC_battery]
            properties, by default None.
        """
        for sheet in self.excel_cells:
            for key, value in self.excel_cells[sheet].items():
                if isinstance(value, dict):
                    battery_number = int(key.replace("Battery ", "")) - 1
                    for battery_key, battery_value_range in value.items():
                        self.batteries[battery_number].set_new_property(
                            sheet,
                            battery_key,
                            self._read_value_direct(
                                sheet, battery_value_range
                            ),
                        )
                else:
                    continue

        if battery_path is not None:
            with open(battery_path, "w", encoding="utf-8") as toml_file:
                for battery in tqdm(
                    self.batteries,
                    "Saving battery configuration for each battery",
                ):
                    for sheet in battery.properties:
                        toml_file.write(f'["{battery.name}"."{sheet}"]\n')
                        for key, value in battery.properties[sheet].items():
                            if value is None:
                                toml_file.write("# ")
                            if isinstance(value, str):
                                toml_file.write(f"'{key}' = '{value}'\n")
                            else:
                                toml_file.write(f"'{key}' = {value}\n")
                    toml_file.write("\n")

    def save_config(
        self, batpac_path: Path = None, battery_path: Path = None
    ) -> None:
        """Save BatPaC_tool configuration

        Read all BatPaC_tool properties and its included [BatPaC_battery]
        properties from the BatPaC Excel tool, save these properties in the
        BatPaC_tool and [BatPaC_battery] objects, and write them as TOML file.

        Parameters
        ----------
        batpac_path : Path, optional
            If specified, storage path to the TOML file for BatPaC_tool
            properties, by default None.
        battery_path : Path, optional
            If specified, storage path to the TOML file for [BatPaC_battery]
            properties, by default None.
        """
        self._save_batpac_config(batpac_path)
        self._save_battery_config(battery_path)
