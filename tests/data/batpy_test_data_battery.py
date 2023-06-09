# -*- coding: UTF-8 -*-
"""Fixed data for tests of the battery
"""


import pytest


@pytest.fixture
def example_battery_data():
    """Validation for battery data"""
    properties = {
        "Dashboard": {
            "Target rated peak power of pack, kW": 200.0,
            "Duration at rated power, s": 10.0,
            "Override duration at rated peak power, s": 5.0,
            "Operating initial SOC for rated peak power, %": 20.0,
            "Override for operating initial SOC for rated peak power, %": 1.0,
            "Total pack capacity, 0-100% SOC (Ah)": 1.0,
            "Total pack energy, 0-100% SOC (kWh)": 40.0,
            "Time to recharge from 15% to 95% SOC, min": 45.0,
            "Optional positive electrode thickness override, µm": 1.0,
            "Average temperature during discharge (default = 30°C), °C": 30.0,
            "Number of cells per module": 20.0,
            "Number of cells in parallel": 2.0,
            "Number of modules in row": 5.0,
            "Number of rows of modules per pack": 4.0,
            "Number of modules in parallel": 400.0,
            "Number of packs manufactured per year": 500000.0,
            "Packs manufactured at 100% utilization (pack/year)": 1.0,
            "Percent plant utilization (%)": 0.95,
        },
        "Battery Design": {
            "Number of packs per vehicle (parallel or series)": 1.0,
            "Parallel (P) or series (S) packs": 1.0,
            "Thickness of cell container aluminum layer (default = 100), µm\
": 100.0,
            "Thickness of cell container PET layer (default = 30), µm": 30.0,
            "Thickness of cell container PP layer (default = 20), µm": 20.0,
            "Width of buffer region for container sealing (default = 6), mm\
": 6.0,
            "Length-to-width ratio for positive electrode (default = 3)": 3.0,
            "Override cell thickness target, mm": 1.0,
            "Thickness of cell edge from positive electrode to outside of \
fold (default = 1), mm": 1.0,
            "Positive terminal material thickness (default = 1.2), mm": 1.2,
            "Negative terminal material thickness (default = 0.8), mm": 0.8,
            "External weld tab length (default = 8), mm": 8.0,
            "Feedthrough length (default = 5), mm": 5.0,
            "Buffer between edge of current collector and edge of internal \
tab (default = 2), mm": 2.0,
            "minimum % OCV at full power, %": 80.0,
            "Cell Interconnects, Thickness of copper interconnects \
(default =1.0), mm": 1.0,
            "Tabs to Module Terminals, Maximum allowable heating rate \
(default = 0.4), °C/s": 0.4,
            "Tabs to Module Terminals, Number per module (default = 2)": 2.0,
            "Module Terminals, Maximum allowable heating rate \
(default = 0.2), °C/s": 0.2,
            "Module Interconnects, Maximum allowable heating rate \
(default = 0.2), °C/s": 0.2,
            "Module Interconnects, Effective conductor length \
(default = 6), cm": 6.0,
            "Bus Bar to Pack Terminal, Maximum allowable heating rate \
(default = 0.04), °C/s": 0.04,
            "Bus Bar for Bridging Module Rows, Maximum allowable heating rate \
(default = 0.04), °C/s": 0.04,
            "Pack Terminals, Maximum allowable heating rate \
(default = 0.04), °C/s": 0.04,
            "Pack Terminals, Effective conductor length \
(default = 12), cm": 12.0,
            "Maximum charger power, kW": 350.0,
            "Charger voltage (default = 480), V": 480.0,
            "Max allowable temperature (default = 55), °C": 55.0,
            "Excess width and length of negative electrode over that of \
positive (default = 2.0), mm": 2.0,
            "Excess width of separator over that of positive \
(default = 2.0), mm": 2.0,
            "Excess length of separator over that of positive \
(default = 6.0), mm": 4.0,
            "Thickness (default = 2), mm": 2.0,
            "Length (default = 35), mm": 35.0,
            "Module wall thickness (default = 0.3), mm": 0.3,
            "Provisions for gas release (default = 5), g": 5.0,
            "Width of space beyond end of cell terminal at back of module \
(default = 2), mm": 2.0,
            "Width of space beyond end of cell terminal at front of module \
(default = 6), mm": 6.0,
            "Thickness of steel rack support channel (default = 1), mm": 1.0,
            "Width of side rails of support channel and upper channel \
(default = 10), mm": 10.0,
            "Thickness of steel in upper rack channel and vertical rack \
members (default = 1), mm": 1.0,
            "Cross-section of vertical rack members (default = 15), mm²": 15.0,
            "Thickness of module restraint plates \
(steel, default = 2), mm": 2.0,
            "Thickness of polymer pads between modules (default = 2), mm": 2.0,
            "Additional rack length for adjustment of module restraint \
(default = 15), mm": 15.0,
            "Additional rack length for bus bars (default = 10), mm": 10.0,
            "Thickness of coolant panel channels (default = 5), mm": 5.0,
            "Thickness of coolant panel walls (default = 0.3), mm": 0.3,
            "Diameter (I.D) of inlet and outlet cooling manifolds \
(0.5-mm wall, default = 25), mm": 25.0,
            "Diameter (I.D) of connecting tubing \
(0.4-mm wall, default = 12), mm": 12.0,
            "Tolerance on interior dimensions (default = 2), mm": 2.0,
            "Pack jacket insulation thickness (default = 10), mm": 10.0,
            "Interior aluminum plate thickness (default = 1), mm": 1.0,
            "Exterior steel plate thickness (default = 1), mm": 1.0,
            "Override angle iron perimeter unit mass, g/mm": 1.0,
            "Pack Jacket Top, Interior aluminum plate thickness \
(default = 1), mm": 1.0,
            "Energy requirement of vehicle on UDDS cycle \
(default = 250), Wh/mile": 250.0,
            "Pack capacity convergence constant": 10772.365447854338,
            "Convergence constant for positive electrode thickness\
": 0.9737462952460316,
            "Convergence constant for cell thickness": 0.1,
        },
        "BMS": {
            "Cells per ASIC": 10.0,
            "BMU PCB mass, (default = 0.04 kg)": 0.04,
            "BMU mass added per ASIC, (default = 0.02 kg)": 0.02,
            "BMU PCB volume (default = 0.16 L)": 0.16,
            "BMU volume added per ASIC (default = 0.08 L)": 0.08,
        },
        "Manufacturing Costs": {
            "Override mass ratio of positive binder solvent to positive binder\
": 1.0,
            "Override mass ratio of negative binder solvent to negative binder\
": 1.0,
            "Errors in unit materials and processing costs \
(default = 10), ±%": 10.0,
            "Errors in electrode thickness and capacity limits \
(default = 5), ±%": 5.0,
        },
        "Thermal": {
            "Coolant temperature at inlet to pack (default = 15), °C": 15.0,
            "Total rise in coolant temperature (default = 5), °C": 5.0,
            "Estimated heat capacity of battery \
(default = 0.85), J/g-°C": 0.85,
            "Energy requirement for pack on UDDS (override), Wh/mile": 1.0,
            "Override battery power for sustained speed": 1.0,
            "Effective ambient temperature (default = 50), °C": 50.0,
            "Thermal conductivity of pack jacket insulation \
(default = 0.00027), W/cm-K": 0.00027,
            "Override heat generation rate, W": 1.0,
            "Thermal conductivity: positive electrode \
(default = 0.013), W/cm-K": 0.013,
            "Thermal conductivity: negative electrode \
(default = 0.013), W/cm-K": 0.013,
            "Thermal conductivity: separator \
(default = 0.002), W/cm-K": 0.002,
            "Thermal conductivity: through folded cell edge \
(default = 0.01), W/cm-K": 0.01,
            "Thermal conductivity: ethylene glycol-50% water solution \
(default = 0.0043), W/cm-K": 0.0043,
            "Coolant heat capacity \
(default = 3.264), J/g-°C": 3.264,
            "Coolant density (ρ, default = 1.07), g/mL": 1.07,
            "Coolant viscosity (µ, default = 0.055), poise (g/s-cm)": 0.055,
            "Estimated additional pressure drop for connections and turns \
(default = 200), %": 200.0,
            "Total efficiency of pump and motor (default = 50), %": 50.0,
            "Battery temperature at startup (default = -15), °C": -15.0,
            "Battery temperature after heating (default = 5), °C": 5.0,
            "Power of heating elements, W": 1000.0,
        },
    }
    return properties
