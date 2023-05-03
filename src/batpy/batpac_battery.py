# -*- coding: UTF-8 -*-
"""Module, which includes the class BatpacBattery
"""
import logging
from pathlib import Path

import toml

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s [%(levelname)s]: \t%(filename)s\t%(funcName)s\t\
        %(lineno)s\t- %(message)s",
    filename="batpy.log",
    filemode="w",
    level=logging.INFO,
)


class BatpacBattery:
    """Battery class for interaction with BatPaC

    This battery class is used to interact with BatPaC and stores battery
    parameters in the dictionary properties.
    """

    def __init__(self, name: str = "Battery") -> None:
        """Initialize battery

        Initialize the battery object.

        Parameters
        ----------
        name : str, optional
            Name of the battery, by default "Battery"

        Examples
        --------
        >>> battery1 = BatPaC_battery("NCM811 - G")
        >>> print(battery1.name)
        "NCM811 - G"

        >>> battery2 = BatPaC_battery()
        >>> print(battery2.name)
        "Battery"
        """
        self.name = name
        logging.info("[ ] Create battery %s", self.name)
        self.properties = {}
        logging.info("[+] Battery %s created", self.name)
        logging.debug(
            "[ ] Properties of battery %s: %s",
            self.name,
            self.properties,
        )

    def load_battery_file(
        self, path_to_battery_file: Path, battery_name: str = "Battery"
    ) -> bool:
        """Load a battery configuration file

        Load the properties for a battery from a TOML battery configuration
        file.

        Parameters
        ----------
        path_to_battery_file : Path
            Path to the TOML battery configuration file.
        battery_name : str, optional
            Name of the table in the TOML file from which to load the battery
            properties. Thereby, the battery_name, by default "Battery", does
            not have to be equal to self.name.

        Returns
        -------
        bool
            True, if battery_name exists in the TOML file and the properties
            were loaded.
            False, if battery_name does not exist in the TOML file and the
            properties could not be loaded.

        Examples
        --------
        battery_config.toml contains a table with the name ["NCM"].
        All key - value pairs are to be loaded for the battery "NCM811 - G".

        >>> battery1 = BatPaC_battery("NCM811 - G")
        >>> battery1.load_battery_file("./battery_config.toml", "NCM")
        """
        logging.info(
            "[ ] Load battery config for %s from %s",
            battery_name,
            path_to_battery_file,
        )
        config = toml.load(path_to_battery_file)
        loaded = False
        if battery_name in config:
            config = config[battery_name]
            for sheet in config:
                for key in config[sheet]:
                    self.set_new_property(sheet, key, config[sheet][key])
            logging.info(
                "[+] Battery config for %s from %s loaded",
                battery_name,
                path_to_battery_file,
            )
            loaded = True
        else:
            logging.warning(
                "[!] No battery config for %s in %s found",
                battery_name,
                path_to_battery_file,
            )
        logging.debug(
            "[ ] Battery properties for %s: %s", self.name, self.properties
        )
        return loaded

    def set_property(self, sheet: str, name: str, value: any) -> None:
        """Set an existing property of the battery

        Set an existing property of the battery in the format
        {"sheet" : {"name" : value} }.

        Parameters
        ----------
        sheet : str
            Name of the BatPaC Excel sheet.
        name : str
            Name of the BatPaC Excel cell description.
        value : any
            Value of the BatPaC Excel cell.
        """
        self.properties[sheet][name] = value

    def get_property(self, sheet: str, name: str) -> any:
        """Get property of the battery

        Get an existing property of the battery.

        Parameters
        ----------
        sheet : str
            Name of the BatPaC Excel sheet.
        name : str
            Name of the BatPaC Excel cell description.

        Returns
        -------
        any
            Value of the stored property.
        """
        return self.properties[sheet][name]

    def set_new_property(self, sheet: str, name: str, value: any) -> None:
        """Set a new property of the battery

        Set an existing property of the battery or create a new one in the
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
