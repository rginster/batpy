# -*- coding: UTF-8 -*-
import xlwings as xw
import toml
from prettytable import PrettyTable
from pathlib import Path
from tqdm import tqdm
import logging
import semantic_version
from typing import Type
import warnings

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s [%(levelname)s]: \t%(filename)s\t%(funcName)s\t%(lineno)s\t- %(message)s",
    filename="batpy.log",
    filemode="w",
    level=logging.INFO,
)


def is_version_compatible(
    self_version: semantic_version.Version,
    version_to_check: semantic_version.Version,
    include_minor: bool = False,
) -> bool:
    if include_minor:
        min_minor = self_version.minor
    else:
        min_minor = 0

    min_version = semantic_version.Version(
        major=self_version.major, minor=min_minor, patch=0
    )

    if min_version <= version_to_check < min_version.next_major():
        logging.info(
            f"[+] Version {version_to_check} is compatible: {min_version} <= {version_to_check} < {min_version.next_major()}"
        )
        return True
    else:
        logging.warning(
            f"[!] Version {version_to_check} should be {min_version} <= {version_to_check} < {min_version.next_major()}"
        )
        raise ValueError(
            f"[!] Version {version_to_check} should be {min_version} <= {version_to_check} < {min_version.next_major()}"
        )


class BatPaC_battery:
    def __init__(self, name: str = "Battery") -> None:
        self.name = name
        logging.info(f"[ ] Create battery {self.name}")
        self.properties = {}
        logging.info(f"[+] Battery {self.name} created")
        logging.debug(f"[ ] Properties of battery {self.name}: {self.properties}")

    def load_battery_file(
        self, path_to_battery_file: Path, battery_name: str = "Battery"
    ) -> bool:
        logging.info(
            f"[ ] Load battery config for {battery_name} from {path_to_battery_file}"
        )
        config = toml.load(path_to_battery_file)
        loaded = False
        if battery_name in config:
            config = config[battery_name]
            for sheet in config:
                for key in config[sheet]:
                    self.set_new_property(sheet, key, config[sheet][key])
            logging.info(
                f"[+] Battery config for {battery_name} from {path_to_battery_file} loaded"
            )
            loaded = True
        else:
            logging.warning(
                f"[!] No battery config for {battery_name} in {path_to_battery_file} found"
            )
        logging.debug(f"[ ] Battery properties for {self.name}: {self.properties}")
        return loaded

    def set_property(self, sheet: str, name: str, value: any) -> None:
        self.properties[sheet][name] = value

    def get_property(self, sheet: str, name: str) -> any:
        return self.properties[sheet][name]

    def set_new_property(self, sheet: str, name: str, value: any) -> None:
        try:
            self.properties[sheet][name] = value
        except:
            self.properties.update({sheet: {name: value}})


class BatPaC_tool:
    def __init__(
        self,
        batpac_workbook_path: Path,
        cell_definition_user_input_toml_path: Path,
        cell_definition_calculation_and_validation_results: Path = None,
        cell_definition_additional_user_input_toml_path: Path = None,
        cell_definition_additional_user_results_toml_path: Path = None,
        excel_visible: bool = False,
    ) -> None:
        logging.info(
            f"[ ] Create BatPaC from {batpac_workbook_path} and load cell references from {cell_definition_user_input_toml_path}"
        )
        self.version = semantic_version.Version("0.1.0")
        self.workbook_path = batpac_workbook_path
        self.toml_path = cell_definition_user_input_toml_path
        self.toml_calculation_validation_results_path = (
            cell_definition_calculation_and_validation_results
        )
        config = toml.load(self.toml_path)
        config_metadata = config.pop("batpy")
        self.batpac_version = config_metadata["BatPaC version"]
        if is_version_compatible(
            self.version, semantic_version.Version(config_metadata["BatPaC SemVer"])
        ):
            self.batpac_semver = semantic_version.Version(
                config_metadata["BatPaC SemVer"]
            )

        self.excel_cells = config
        self.batteries = list()
        self.wb = xw.Book(batpac_workbook_path)
        self.app = self.wb.app
        self.app.visible = excel_visible
        self.max_batteries = 7
        self.properties = {}
        logging.info(
            f"[+] Created BatPaC version {self.batpac_version} (SemVer: {self.batpac_semver}) from {self.workbook_path} and load cell references from {self.toml_path}"
        )

    def __del__(self) -> None:
        try:
            self.wb.app.calculation = "automatic"
            self.wb.app.screen_updating = True
        except:
            pass

    def is_version_compatible(
        self, version_to_check: semantic_version.Version, include_minor: bool = False
    ) -> bool:
        return is_version_compatible(self.version, version_to_check, include_minor)

    def load_batpac_file(self, path_to_batpac_file: Path) -> None:
        logging.info(f"[ ] Load BatPaC file from {path_to_batpac_file}")
        self.properties = toml.load(path_to_batpac_file)
        logging.info(f"[+] Loaded BatPaC file from {path_to_batpac_file}")
        logging.debug(f"[ ] BatPaC properties {self.properties}")

    def add_battery(self, batteries: list[BatPaC_battery]) -> None:
        for battery in batteries:
            if len(self.batteries) + 1 <= self.max_batteries:
                self.batteries.append(battery)
            else:
                print(
                    f"Battery {battery.name} ({battery}) exceeds the limit of batteries for a single workbook"
                )
                logging.warning(
                    f"[!] Battery {battery.name} ({battery}) exceeds the limit of batteries for a single workbook"
                )

    def set_new_property(self, sheet: str, name: str, value: any) -> None:
        try:
            self.properties[sheet][name] = value
        except:
            self.properties.update({sheet: {name: value}})

    def load_batteries_file(
        self, path_to_batteries_file: Path, batteries: list
    ) -> None:
        logging.info(f"[ ] Load batteries from file {path_to_batteries_file}")
        self.batteries.clear()
        self.add_battery(batteries)
        for battery in self.batteries:
            battery.load_battery_file(path_to_batteries_file, battery.name)
            logging.debug(f"[ ] Battery {battery.name} properties {battery.properties}")
        logging.info(f"[+] Batteries from file {path_to_batteries_file} loaded")

    def write_value_direct(self, worksheet: str, range: str, value) -> None:
        self.wb.sheets[worksheet][range].value = value

    def read_value_direct(self, worksheet: str, range: str) -> any:
        try:
            value = self.wb.sheets[worksheet][range].value
            return value
        except:
            logging.warning(f"[!] Key {worksheet} , {range} not found")
            raise KeyError

    def wb_helper_range(
        self,
        worksheet: str,
        name: str,
        battery: BatPaC_battery = None,
        additional_cell_config: Path | dict = None,
    ) -> str | bool:
        try:
            if additional_cell_config is not None:
                if type(additional_cell_config) is Path:
                    additional_cell_config = toml.load(additional_cell_config)
                range_dict = additional_cell_config
            else:
                range_dict = self.excel_cells

            if battery is None:
                range = range_dict[worksheet][name]
            else:
                range = range_dict[worksheet][
                    "Battery " + str(self.batteries.index(battery) + 1)
                ][name]
            return range
        except:
            logging.warning(f"[!] Key {worksheet} , {name} not found")
            raise KeyError

    def write_value(self, worksheet: str, name: str, value) -> None:
        self.write_value_direct(worksheet, self.wb_helper_range(worksheet, name), value)
        logging.debug(
            f"[ ] Write in {worksheet} {self.wb_helper_range(worksheet, name)} ({name}) = {value}"
        )

    def read_value(
        self, worksheet: str, name: str, additional_cell_config: Path | dict = None
    ) -> str | bool:
        return self.read_value_direct(
            worksheet,
            self.wb_helper_range(
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
        battery: BatPaC_battery,
        additional_cell_config: Path | dict = None,
    ) -> str | bool:
        return self.read_value_direct(
            worksheet,
            self.wb_helper_range(worksheet, name, battery, additional_cell_config),
        )

    def write_value_battery(
        self, worksheet: str, name: str, battery: BatPaC_battery, value: any
    ) -> None:
        self.write_value_direct(
            worksheet, self.wb_helper_range(worksheet, name, battery), value
        )
        logging.debug(
            f"[ ] Write for {battery.name} in {worksheet} {self.wb_helper_range(worksheet, name, battery)} ({name}) = {value}"
        )

    def stop_automatic_calculation(self) -> None:
        self.write_value("Dashboard", "Restart (0/1)", 0)
        self.wb.app.calculation = "manual"
        self.wb.app.screen_updating = False

    def start_automatic_calculation(self) -> None:
        reset_macro = self.wb.macro("Module1.Reset")
        reset_macro()
        self.wb.app.calculation = "automatic"
        self.wb.app.screen_updating = True

    def read_from_user_input(user_read_file: Path) -> dict:
        warnings.warn("This function is not implemented.")
        if user_read_file.is_file():
            return True
        else:
            logging.warning(f"[!] {user_read_file} is not a valid file")
            raise ValueError(f"{user_read_file} is not a valid file")

    def read_calculation_and_validation_results(
        self, toml_file_calculation_validation_results: Path = None
    ) -> dict | bool:
        if toml_file_calculation_validation_results is None:
            if self.toml_calculation_validation_results_path is None:
                logging.warning(
                    f"[!] No toml file for calculation and validation found"
                )
                return False
        else:
            self.toml_calculation_validation_results_path = (
                toml_file_calculation_validation_results
            )

        additional_cell_config = toml.load(
            self.toml_calculation_validation_results_path
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
                    additional_cell_config,
                )
            )
            config_warnings.append(
                self.read_value_battery(
                    "Dashboard",
                    "Configuration Warnings (see table  to right)",
                    battery,
                    additional_cell_config,
                )
            )
            plant_size.append(
                self.read_value_battery(
                    "Dashboard", "Plant Size, GWh", battery, additional_cell_config
                )
            )
            power_to_energy.append(
                self.read_value_battery(
                    "Dashboard",
                    "Power-to-energy ratio",
                    battery,
                    additional_cell_config,
                )
            )
            adequacy_cooling.append(
                self.read_value_battery(
                    "Dashboard", "Adequacy of cooling", battery, additional_cell_config
                )
            )
            cathode_thickness.append(
                self.read_value_battery(
                    "Dashboard",
                    "Cathode thickness limited by",
                    battery,
                    additional_cell_config,
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
            f"[ ] Sheets type is {type(sheets)} and sheets available: {sheets}"
        )

        for sheet in tqdm(sheets, "Processing battery configuration in each sheet"):
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
        logging.info("[ ] Save workbook")
        if path is None:
            path = self.workbook_path
        self.wb.save(path)
        self.wb = xw.Book(path)
        self.app = self.wb.app
        logging.info(f"[+] Saved workbook in {path}")

    def close(self) -> bool:
        if len(self.wb.app.books) == 1:
            self.wb.app.quit()
            logging.info("[+] Workbook and Excel closed")
            return True
        else:
            self.wb.close()
            logging.info("[+] Workbook closed")
            return True

    def save_config(self, batpac_path: Path = None, battery_path: Path = None) -> None:
        for sheet in self.excel_cells:
            for key, value in self.excel_cells[sheet].items():
                if type(value) is dict:
                    battery_number = int(key.replace("Battery ", "")) - 1
                    for battery_key, battery_value_range in value.items():
                        self.batteries[battery_number].set_new_property(
                            sheet,
                            battery_key,
                            self.read_value_direct(sheet, battery_value_range),
                        )
                else:
                    self.set_new_property(sheet, key, self.read_value(sheet, key))

        if batpac_path is not None:
            with open(batpac_path, "w") as toml_file:
                for sheet in tqdm(
                    self.properties, "Saving BatPaC config from each sheet"
                ):
                    toml_file.write(f'["{sheet}"]\n')
                    for key, value in self.properties[sheet].items():
                        if value is None or key == "Restart (0/1)":
                            toml_file.write("# ")
                        if type(value) is str:
                            toml_file.write(f"'{key}' = '{value}'\n")
                        else:
                            toml_file.write(f"'{key}' = {value}\n")
                    toml_file.write("\n")

        if battery_path is not None:
            with open(battery_path, "w") as toml_file:
                for battery in tqdm(
                    self.batteries, "Saving battery configuration for each battery"
                ):
                    for sheet in battery.properties:
                        toml_file.write(f'["{battery.name}"."{sheet}"]\n')
                        for key, value in battery.properties[sheet].items():
                            if value is None:
                                toml_file.write("# ")
                            if type(value) is str:
                                toml_file.write(f"'{key}' = '{value}'\n")
                            else:
                                toml_file.write(f"'{key}' = {value}\n")
                    toml_file.write("\n")
