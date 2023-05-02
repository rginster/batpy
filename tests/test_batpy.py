# -*- coding: UTF-8 -*-
from batpy import BatPaC_battery, BatPaC_tool, is_version_compatible
import xlwings as xw
import toml
import pytest
import pathlib
import semantic_version


@pytest.fixture
def example_battery_data():
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
            "Thickness of cell container aluminum layer (default = 100), µm": 100.0,
            "Thickness of cell container PET layer (default = 30), µm": 30.0,
            "Thickness of cell container PP layer (default = 20), µm": 20.0,
            "Width of buffer region for container sealing (default = 6), mm": 6.0,
            "Length-to-width ratio for positive electrode (default = 3)": 3.0,
            "Override cell thickness target, mm": 1.0,
            "Thickness of cell edge from positive electrode to outside of fold (default = 1), mm": 1.0,
            "Positive terminal material thickness (default = 1.2), mm": 1.2,
            "Negative terminal material thickness (default = 0.8), mm": 0.8,
            "External weld tab length (default = 8), mm": 8.0,
            "Feedthrough length (default = 5), mm": 5.0,
            "Buffer between edge of current collector and edge of internal tab (default = 2), mm": 2.0,
            "minimum % OCV at full power, %": 80.0,
            "Cell Interconnects, Thickness of copper interconnects (default =1.0), mm": 1.0,
            "Tabs to Module Terminals, Maximum allowable heating rate (default = 0.4), °C/s": 0.4,
            "Tabs to Module Terminals, Number per module (default = 2)": 2.0,
            "Module Terminals, Maximum allowable heating rate (default = 0.2), °C/s": 0.2,
            "Module Interconnects, Maximum allowable heating rate (default = 0.2), °C/s": 0.2,
            "Module Interconnects, Effective conductor length (default = 6), cm": 6.0,
            "Bus Bar to Pack Terminal, Maximum allowable heating rate (default = 0.04), °C/s": 0.04,
            "Bus Bar for Bridging Module Rows, Maximum allowable heating rate (default = 0.04), °C/s": 0.04,
            "Pack Terminals, Maximum allowable heating rate (default = 0.04), °C/s": 0.04,
            "Pack Terminals, Effective conductor length (default = 12), cm": 12.0,
            "Maximum charger power, kW": 350.0,
            "Charger voltage (default = 480), V": 480.0,
            "Max allowable temperature (default = 55), °C": 55.0,
            "Excess width and length of negative electrode over that of positive (default = 2.0), mm": 2.0,
            "Excess width of separator over that of positive (default = 2.0), mm": 2.0,
            "Excess length of separator over that of positive (default = 6.0), mm": 4.0,
            "Thickness (default = 2), mm": 2.0,
            "Length (default = 35), mm": 35.0,
            "Module wall thickness (default = 0.3), mm": 0.3,
            "Provisions for gas release (default = 5), g": 5.0,
            "Width of space beyond end of cell terminal at back of module (default = 2), mm": 2.0,
            "Width of space beyond end of cell terminal at front of module (default = 6), mm": 6.0,
            "Thickness of steel rack support channel (default = 1), mm": 1.0,
            "Width of side rails of support channel and upper channel (default = 10), mm": 10.0,
            "Thickness of steel in upper rack channel and vertical rack members (default = 1), mm": 1.0,
            "Cross-section of vertical rack members (default = 15), mm²": 15.0,
            "Thickness of module restraint plates (steel, default = 2), mm": 2.0,
            "Thickness of polymer pads between modules (default = 2), mm": 2.0,
            "Additional rack length for adjustment of module restraint (default = 15), mm": 15.0,
            "Additional rack length for bus bars (default = 10), mm": 10.0,
            "Thickness of coolant panel channels (default = 5), mm": 5.0,
            "Thickness of coolant panel walls (default = 0.3), mm": 0.3,
            "Diameter (I.D) of inlet and outlet cooling manifolds (0.5-mm wall, default = 25), mm": 25.0,
            "Diameter (I.D) of connecting tubing (0.4-mm wall, default = 12), mm": 12.0,
            "Tolerance on interior dimensions (default = 2), mm": 2.0,
            "Pack jacket insulation thickness (default = 10), mm": 10.0,
            "Interior aluminum plate thickness (default = 1), mm": 1.0,
            "Exterior steel plate thickness (default = 1), mm": 1.0,
            "Override angle iron perimeter unit mass, g/mm": 1.0,
            "Pack Jacket Top, Interior aluminum plate thickness (default = 1), mm": 1.0,
            "Energy requirement of vehicle on UDDS cycle (default = 250), Wh/mile": 250.0,
            "Pack capacity convergence constant": 10772.365447854338,
            "Convergence constant for positive electrode thickness": 0.9737462952460316,
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
            "Override mass ratio of positive binder solvent to positive binder": 1.0,
            "Override mass ratio of negative binder solvent to negative binder": 1.0,
            "Errors in unit materials and processing costs (default = 10), ±%": 10.0,
            "Errors in electrode thickness and capacity limits (default = 5), ±%": 5.0,
        },
        "Thermal": {
            "Coolant temperature at inlet to pack (default = 15), °C": 15.0,
            "Total rise in coolant temperature (default = 5), °C": 5.0,
            "Estimated heat capacity of battery (default = 0.85), J/g-°C": 0.85,
            "Energy requirement for pack on UDDS (override), Wh/mile": 1.0,
            "Override battery power for sustained speed": 1.0,
            "Effective ambient temperature (default = 50), °C": 50.0,
            "Thermal conductivity of pack jacket insulation (default = 0.00027), W/cm-K": 0.00027,
            "Override heat generation rate, W": 1.0,
            "Thermal conductivity: positive electrode (default = 0.013), W/cm-K": 0.013,
            "Thermal conductivity: negative electrode (default = 0.013), W/cm-K": 0.013,
            "Thermal conductivity: separator (default = 0.002), W/cm-K": 0.002,
            "Thermal conductivity: through folded cell edge (default = 0.01), W/cm-K": 0.01,
            "Thermal conductivity: ethylene glycol-50% water solution (default = 0.0043), W/cm-K": 0.0043,
            "Coolant heat capacity (default = 3.264), J/g-°C": 3.264,
            "Coolant density (ρ, default = 1.07), g/mL": 1.07,
            "Coolant viscosity (µ, default = 0.055), poise (g/s-cm)": 0.055,
            "Estimated additional pressure drop for connections and turns (default = 200), %": 200.0,
            "Total efficiency of pump and motor (default = 50), %": 50.0,
            "Battery temperature at startup (default = -15), °C": -15.0,
            "Battery temperature after heating (default = 5), °C": 5.0,
            "Power of heating elements, W": 1000.0,
        },
    }
    return properties


@pytest.fixture
def example_batpac_data():
    properties = {
        "Dashboard": {
            "Electrode Couple": "NMC811-G (Energy)",
            "Positive active material specific capacity, mAh/g": 200.0,
            "Void volume fraction, % of positive electrode": 20.0,
            "Positive foil thickness, mm": 10.0,
            "Maximum positive electrode thickness, µm": 110.0,
            # 'Restart (0/1)' : 1.0,
            # 'Negative active material specific capacity, mAh/g' : None,
            # 'N/P capacity ratio after formation' : None,
            # 'Void volume fraction, % of negative electrode' : None,
            # 'Negative current collector thickness, µm' : None,
            # 'Separator thickness, µm' : None,
            "Vehicle Type": "EV",
            "Calculate Charging Requirements?": "Yes",
            # 'OEM Upper Cuttoff SOC' : None,
            # 'OEM Lower Cutoff SOC' : None,
            "Use default power requirements for vehicle": "Yes",
            # 'Al foil, $/m²' : None,
            # 'Cu foil, $/m²' : None,
            # 'Separator, $/m²' : None,
            # 'Electrolyte, $/L' : None,
            "Method to calculate plant utilization": "Method 1: Ignore utilization",
            "Cell yield, % of built cells that pass inspection": 95.0,
            "Method for manufacturing pack": "All manufacturing in-house (Default)",
            "Option for pack cost": "Cost to consumer - includes pack profit/warranty (Default)",
            "Unit": "Absolute",
            "X =": "Battery system rated power, kW",
            "Y1 =": "Positive electrode thickness, µm",
            "Y2 =": "Cell cost, $/kWh",
            # 'Positive Electrode, $/kg, Active material, $/kg' : None,
            # 'Positive Electrode, $/kg, Carbon additive, $/kg' : None,
            # 'Positive Electrode, $/kg, Binder, $/kg' : None,
            # 'Positive Electrode, $/kg, Solvent (NMP), $/kg' : None,
            # 'Negative electrode, $/kg, Active material, $/kg' : None,
            # 'Negative electrode, $/kg, Carbon additive, $/kg' : None,
            # 'Negative electrode, $/kg, Binder, $/kg' : None,
            # 'Negative electrode, $/kg, Solvent (Water), $/kg' : None,
        },
        "Chem": {
            # 'Couple Name' : None,
            "Positive Electrode Active Material": "NMC911",
            # 'Positive electrode active material capacity, mAh/g:' : None,
            # 'Positive electrode active material weight %' : None,
            # 'Positive electrode carbon addtive weight %' : None,
            # 'Positive electrode binder weight %' : None,
            # 'Binder solvent for positive electrode' : None,
            # 'Positive electrode active material density, g/cm³' : None,
            # 'Positive electrode carbon additive density, g/cm³' : None,
            # 'Positive electrode binder density, g/cm³' : None,
            # 'Positive electrode porosity, volume % of void space' : None,
            # 'Positive electrode specific particle area "a", cm²/cm³' : None,
            # 'Positive electrode active material exchange current, i0, mA/cm2' : None,
            # 'Maximum thickness limit for positive electrode, mm' : None,
            # 'Minimum thickness limit for positive electrode, mm' : None,
            # 'Positive foil material' : None,
            # 'Positive foil thickness, µm' : None,
            # 'Add 5% silicon to negative electrode?' : None,
            # 'Negative Electrode Active Material' : None,
            # 'Negative-to-positive capacity ratio after formation' : None,
            # 'Negative electrode active material capacity, mAh/g:' : None,
            # 'Negative electrode active weight %' : None,
            # 'Negative electrode carbon addtive weight %' : None,
            # 'Negative electrode binder weight %' : None,
            # 'Binder solvent for negative electrode' : None,
            # 'Negative electrode active material density, g/cm³' : None,
            # 'Negative electrode carbon additive density, g/cm³' : None,
            # 'Negative electrode binder density, g/cm³' : None,
            # 'Negative electrode porosity, volume % of void space' : None,
            # 'Negative electrode specific area "a", cm²/cm³' : None,
            # 'Negative electrode active material exchange current, i0, mA/cm2' : None,
            # 'Negative foil material' : None,
            # 'Negative foil thickness, µm' : None,
            # 'Separator thickness, µm' : None,
            # 'Separator porosity, volume % of void space' : None,
            # 'Separator density, g/cm³' : None,
            # 'Electrolyte density, g/cm³' : None,
            # 'Electrolyte (1.2M LiPF6), g Li/L electrolyte' : None,
            # 'Limiting current for ionic diffuison' : None,
            # 'Additive for the positive electrode, Additive name' : None,
            # 'Additive for the positive electrode, Additive weight percentage, % of total positive electrode material mass' : None,
            # 'Additive for the positive electrode, Lithium mass fraction in additive, %' : None,
            # 'Additive for the positive electrode, Price of additive, $/kg' : None,
            # 'Additive for the negative electrode, Additive name' : None,
            # 'Additive for the negative electrode, Additive weight percentage, % of total negative electrode material mass' : None,
            # 'Additive for the negative electrode, Lithium mass fraction in additive, %' : None,
            # 'Additive for the negative electrode, Price of additive, $/kg' : None,
            # 'Additive for the Electrolyte, Additive name' : None,
            # 'Additive for the Electrolyte, Additive weight percentage, % of total electrolyte mass' : None,
            # 'Additive for the Electrolyte, Lithium mass fraction in additive, %' : None,
            # 'Additive for the Electrolyte, Price of additive, $/kg' : None,
            # 'Maximum charging current density, mA/cm²' : None,
            # 'Open circuit voltage at 0% SOC, V' : None,
            # 'Open circuit voltage at 10% SOC, V' : None,
            # 'Open circuit voltage at 20% SOC, V' : None,
            # 'Open circuit voltage at 30% SOC, V' : None,
            # 'Open circuit voltage at 40% SOC, V' : None,
            # 'Open circuit voltage at 50% SOC, V' : None,
            # 'Open circuit voltage at 60% SOC, V' : None,
            # 'Open circuit voltage at 70% SOC, V' : None,
            # 'Open circuit voltage at 80% SOC, V' : None,
            # 'Open circuit voltage at 90% SOC, V' : None,
            # 'Open circuit voltage at 100% SOC, V' : None,
            # 'Area specific impedance at 2-sec burst, 0% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 2-sec burst, 10% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 2-sec burst, 20% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 2-sec burst, 30% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 2-sec burst, 40% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 2-sec burst, 50% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 2-sec burst, 60% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 2-sec burst, 70% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 2-sec burst, 80% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 2-sec burst, 90% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 2-sec burst, 100% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 10-sec burst, 0% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 10-sec burst, 10% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 10-sec burst, 20% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 10-sec burst, 30% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 10-sec burst, 40% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 10-sec burst, 50% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 10-sec burst, 60% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 10-sec burst, 70% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 10-sec burst, 80% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 10-sec burst, 90% SOC, ohm-cm²' : None,
            # 'Area specific impedance at 10-sec burst, 100% SOC, ohm-cm²' : None,
            # 'Positive electrode capacity at default ASI, mAh/cm2' : None,
            # 'Positive electrode thickness at default ASI, µm' : None,
            # 'Negative electrode thickness at default ASI, µm' : None,
            # 'Pulse C-rate at default ASI, A/Ah' : None,
            # 'ASI associated with positive interfacial effects, ohm-cm²' : None,
            # 'ASI associated with negative interfacial effects, ohm-cm²' : None,
            # 'Solid state diffusion limiting C-rate (10-s), A/Ah' : None,
            # 'Effective activation energy for ASI calculations (kJ/mole)' : None,
            # 'Cost of active material for positive electrode, $/kg' : None,
            # 'Cost of carbon additive for positive electrode, $/kg' : None,
            # 'Cost of binder for positive electrode $/kg' : None,
            # 'Cost of solvent of positive electrode $/kg' : None,
            # 'Cost of active material for negative electrode, $/kg' : None,
            # 'Cost of carbon additive for negative electrode, $/kg' : None,
            # 'Cost of binder for negative electrode $/kg' : None,
            # 'Cost of solvent of negative electrode $/kg' : None,
            # 'Positive current collector foil, $/m²' : None,
            # 'Negative current collector foil, $/m²' : None,
            # 'Separators, $/m²' : None,
            # 'Electrolyte, $/L' : None,
        },
        "BMS": {"p-factor for most electronic components": 0.9},
        "Cost Input": {
            "Effective Yield Across All Steps, Binder (NMP) solvent recovery, %": 99.5,
            "Mixing, Positive electrode material, dry (default = 99, 95, 99, 99, -), %": 99.0,
            "Mixing, Negative electrode material, dry (defulat = 99, 95, 99, 99, -), %": 99.0,
            "Coating, Positive electrode material, dry (default = 99, 95, 99, 99, -), %": 95.0,
            "Coating, Negative electrode material, dry (defulat = 99, 95, 99, 99, -), %": 95.0,
            "Coating, Positive current collector foil (default = -, 95, 92, 99, -), %": 95.0,
            "Coating, Negative current collector foil (default = -, 95, 92, 99, -), %": 95.0,
            "Electrode Slitting, Positive electrode material, dry (default = 99, 95, 99, 99, -), %": 99.0,
            "Electrode Slitting, Negative electrode material, dry (defulat = 99, 95, 99, 99, -), %": 99.0,
            "Electrode Slitting, Positive current collector foil (default = -, 95, 92, 99, -), %": 92.0,
            "Electrode Slitting, Negative current collector foil (default = -, 95, 92, 99, -), %": 92.0,
            "Cell Stacking, Positive electrode material, dry (default = 99, 95, 99, 99, -), %": 99.0,
            "Cell Stacking, Negative electrode material, dry (defulat = 99, 95, 99, 99, -), %": 99.0,
            "Cell Stacking, Positive current collector foil (default = -, 95, 92, 99, -), %": 99.0,
            "Cell Stacking, Negative current collector foil (default = -, 95, 92, 99, -), %": 99.0,
            "Cell Stacking, Separators (default = -, -, -, 98, -), %": 98.0,
            "Electrolyte Filling, Electrolyte (default = -, -, -, -, 99), %": 99.0,
            "Positive Electrode, $/kg, Active material, $/kg": 1.0,
            "Positive Electrode, $/kg, Conductive additive, $/kg": 1.0,
            "Positive Electrode, $/kg, Binder, $/kg": 1.0,
            "Positive Electrode, $/kg, Binder solvent, $/kg": 1.0,
            "Negative electrode material, $/kg, Active material, $/kg": 1.0,
            "Negative electrode material, $/kg, Conductive additive, $/kg": 1.0,
            "Negative electrode material, $/kg, Binder, $/kg": 1.0,
            "Negative electrode material, $/kg, Binder solvent, $/kg": 1.0,
            "Additional Components, Positive current collector foil, $/m²": 1.0,
            "Additional Components, Negative current collector foil, $/m²": 1.0,
            "Additional Components, Separators, $/m²": 1.0,
            "Additional Components, Electrolyte, $/L": 1.0,
            "Cost per Mass, $/kg, Positive terminal, (default = 2.41, 0.08)": 2.4050000000000002,
            "Cost per Mass, $/kg, Negative terminal, (default = 8.64, 0.08)": 8.64,
            "Cost per Mass, $/kg, Cell Container (default = 3, 0.2)": 3.0,
            "Cost per Mass, $/kg, Heat conductor, (default = 2.41, 0.15)": 2.4050000000000002,
            "Plus Cost per Cell*, $, Positive terminal, (default = 2.41, 0.08)": 0.08,
            "Plus Cost per Cell*, $, Negative terminal, (default = 8.64, 0.08)": 0.08,
            "Plus Cost per Cell*, $, Cell Container (default = 3, 0.2)": 0.2,
            "Plus Cost per Cell*, $, Heat conductor, (default = 2.41, 0.15)": 0.15,
            'Plus Cost per Cell*, $, *Scale exponent for "plus cost," p (default = 0.85)': 0.85,
            "Cost per Parallel Unit, $, Module management system, MMS (default = 2, 0.03)": 2.0,
            "Cost per Module Capacity, $/Ah, Module management system, MMS (default = 2, 0.03)": 0.03,
            "Cost per Mass, $/kg, Cell interconnect (default = 8.72, 0.04)": 8.72,
            "Cost per Mass, $/kg, Interconnect panel (default = 2.3, 0.2)": 2.3,
            "Cost per Mass, $/kg, Module terminal (default = 8.64, 0.35)": 8.64,
            "Cost per Mass, $/kg, Module enclosure materials (default = 2.4, 0.5)": 2.4,
            "Cost per Mass, $/kg, Provision for gas release (default = 0, 0.5), $/module": 0.0,
            "Plus Cost per Item*, $, Cell interconnect (default = 8.72, 0.04)": 0.04,
            "Plus Cost per Item*, $, Interconnect panel (default = 2.3, 0.2)": 0.2,
            "Plus Cost per Item*, $, Module terminal (default = 8.64, 0.35)": 0.18,
            "Plus Cost per Item*, $, Module enclosure materials (default = 2.4, 0.5)": 0.5,
            "Plus Cost per Item*, $, Provision for gas release (default = 0, 0.5), $/module": 0.5,
            "Cost per Mass, $/kg, Row rack (default = 1.33, 1)": 1.325,
            "Cost per Mass, $/kg, Pads between modules (default = 1, 0.2)": 1.0,
            "Cost per Mass, $/kg, Module Interconnects and signal wiring (default = 8.52, 0.4)": 8.84,
            "Cost per Mass, $/kg, Bus bars (default = 8.36, 0.6)": 8.68,
            "Cost per Mass, $/kg, Cooling panels (default = 2.8, 0.5)": 2.8000000000000003,
            "Cost per Mass, $/kg, Coolant manifolds (default = 8, 1)": 8.0,
            "Cost per Mass, $/kg, Pack terminals and seals (default = 8.56, 0.75)": 8.88,
            "Cost per Mass, $/kg, Pack jacket steel (default = 1.4, 3)": 1.4000000000000001,
            "Cost per Mass, $/kg, Pack jacket aluminum (default = 2.81, 3)": 2.805,
            "Plus Cost per Item*, $, Row rack (default = 1.33, 1)": 1.0,
            "Plus Cost per Item*, $, Pads between modules (default = 1, 0.2)": 0.2,
            "Plus Cost per Item*, $, Module Interconnects and signal wiring (default = 8.52, 0.4)": 0.4,
            "Plus Cost per Item*, $, Bus bars (default = 8.36, 0.6)": 0.6,
            "Plus Cost per Item*, $, Cooling panels (default = 2.8, 0.5)": 0.5,
            "Plus Cost per Item*, $, Coolant manifolds (default = 8, 1)": 1.0,
            "Plus Cost per Item*, $, Pack terminals and seals (default = 8.56, 0.75)": 0.75,
            "Plus Cost per Item*, $, Pack jacket steel (default = 1.4, 3)": 3.0,
            "Plus Cost per Item*, $, Pack jacket aluminum (default = 2.81, 3)": 3.0,
            "Pack jacket insulation (default = 3), $/m²": 3.0,
            '*Scale exponent for "plus cost" (p) (default = 0.85)': 0.85,
            "Effective full days of operation per year (default = 320)": 320.0,
            "Cost of land and building (default = 3000), $/m²": 3000.0,
            "Launch cost rates, Percent of direct annual materials and purch. items cost (default = 5), %": 5.0,
            "Launch cost rates, Percent of direct labor plus variable overhead (default = 10), %": 10.0,
            "Working capital, percent of annual variable cost (default = 15), %": 15.0,
            "Direct labor rate (default = 25), $/hr": 25.0,
            "Variable overhead rate, % of direct labor (default = 40)": 40.0,
            "Variable overhead rate, % of depreciation (default = 20)": 20.0,
            "General, Sales, Administration rates, Percent of direct labor plus variable overhead (default = 25), %": 25.0,
            "General, Sales, Administration rates, Percent of depreciation (default = 25), %": 25.0,
            "Research and development rate (default = 40), % of depreciation": 40.0,
            "Depreciation rates, Lifetime of capital equipment for straight line depreciation (default = 10), years": 10.0,
            "Depreciation rates, Percent of building investment (default = 5), %": 5.0,
            "Cell profits (default = 5), % of investment": 5.0,
            "Cell warranty cost (default = 5.6), % of cell cost added to price": 5.6,
            "Module profits (default = 5), % of investment": 5.0,
            "Module warranty cost (default = 5.6), % of module cost added to price": 5.6,
            "Pack profits (default = 5), % of investment": 5.0,
            "Pack warranty costs (default = 5.6), % of pack cost added to price": 5.6,
            "Baseline Plant, Materials preparation and delivery to coating, Positive materials, Direct labor, hours/year": 200000.0,
            "Baseline Plant, Materials preparation and delivery to coating, Positive materials, Capital equipment, million$": 200.0,
            "Baseline Plant, Materials preparation and delivery to coating, Positive materials, Plant area, m²": 8000.0,
            "Baseline Plant, Materials preparation and delivery to coating, Negative materials, Direct labor, hours/year": 270000.0,
            "Baseline Plant, Materials preparation and delivery to coating, Negative materials, Capital equipment, million$": 280.0,
            "Baseline Plant, Materials preparation and delivery to coating, Negative materials, Plant area, m²": 8800.0,
            "Baseline Plant, Electrode coating, Positive materials, Solvent evaporated, kg/m²yr": 0.11950458192929046,
            "Baseline Plant, Electrode coating, Positive materials, Direct labor, hours/year": 59000.0,
            "Baseline Plant, Electrode coating, Positive materials, Capital equipment, million$": 90.0,
            "Baseline Plant, Electrode coating, Positive materials, Plant area, m²": 16000.0,
            "Baseline Plant, Electrode coating, Negative materials, Solvent evaporated, kg/m²yr": 0.0793075777152315,
            "Baseline Plant, Electrode coating, Negative materials, Direct labor, hours/year": 59000.0,
            "Baseline Plant, Electrode coating, Negative materials, Capital equipment, million$": 78.0,
            "Baseline Plant, Electrode coating, Negative materials, Plant area, m²": 16000.0,
            "Baseline Plant, Calendering, Positive materials, Direct labor, hours/year": 61000.0,
            "Baseline Plant, Calendering, Positive materials, Capital equipment, million$": 25.0,
            "Baseline Plant, Calendering, Positive materials, Plant area, m²": 2100.0,
            "Baseline Plant, Calendering, Negative materials, Direct labor, hours/year": 69000.0,
            "Baseline Plant, Calendering, Negative materials, Capital equipment, million$": 25.0,
            "Baseline Plant, Calendering, Negative materials, Plant area, m²": 2100.0,
            "Baseline Plant, Notching, Positive materials, Direct labor, hours/year": 250000.0,
            "Baseline Plant, Notching, Positive materials, Capital equipment, million$": 29.0,
            "Baseline Plant, Notching, Positive materials, Plant area, m²": 3200.0,
            "Baseline Plant, Notching, Negative materials, Direct labor, hours/year": 250000.0,
            "Baseline Plant, Notching, Negative materials, Capital equipment, million$": 29.0,
            "Baseline Plant, Notching, Negative materials, Plant area, m²": 3200.0,
            "Baseline Plant, Vacuum Drying of Electrodes, Positive materials, Direct labor, hours/year": 41000.0,
            "Baseline Plant, Vacuum Drying of Electrodes, Positive materials, Capital equipment, million$": 14.0,
            "Baseline Plant, Vacuum Drying of Electrodes, Positive materials, Plant area, m²": 2000.0,
            "Baseline Plant, Vacuum Drying of Electrodes, Negative materials, Direct labor, hours/year": 35000.0,
            "Baseline Plant, Vacuum Drying of Electrodes, Negative materials, Capital equipment, million$": 11.0,
            "Baseline Plant, Vacuum Drying of Electrodes, Negative materials, Plant area, m²": 1600.0,
            "Baseline Plant, Electrode Slitting (positive and negative), Direct labor, hours/year": 260000.0,
            "Baseline Plant, Electrode Slitting (positive and negative), Capital equipment, million$": 30.0,
            "Baseline Plant, Electrode Slitting (positive and negative), Plant area, m²": 0.0,
            "Baseline Plant, Cell stacking, Baseline Cell Capacity, Ah": 68.0,
            "Baseline Plant, Cell stacking, Direct labor, hours/year": 700000.0,
            "Baseline Plant, Cell stacking, Capital equipment, million$": 170.0,
            "Baseline Plant, Cell stacking, Plant area, m²": 0.0,
            "Baseline Plant, Current collector welding, Direct labor, hours/year": 190000.0,
            "Baseline Plant, Current collector welding, Capital equipment, million$": 190.0,
            "Baseline Plant, Current collector welding, Plant area, m²": 0.0,
            "Baseline Plant, X-ray inspection, Direct labor, hours/year": 190000.0,
            "Baseline Plant, X-ray inspection, Capital equipment, million$": 14.0,
            "Baseline Plant, X-ray inspection, Plant area, m²": 0.0,
            "Baseline Plant, Inserting cell in container, Direct labor, hours/year": 49000.0,
            "Baseline Plant, Inserting cell in container, Capital equipment, million$": 11.0,
            "Baseline Plant, Inserting cell in container, Plant area, m²": 0.0,
            "Baseline Plant, Electrolyte filling and cell sealing, Direct labor, hours/year": 132000.0,
            "Baseline Plant, Electrolyte filling and cell sealing, Capital equipment, million$": 25.0,
            "Baseline Plant, Electrolyte filling and cell sealing, Plant area, m²": 0.0,
            "Baseline Plant, Dry room (area included for all cell assembly steps), Direct labor, hours/year": 8000.0,
            "Baseline Plant, Dry room (area included for all cell assembly steps), Capital equipment, million$": 7.3,
            "Baseline Plant, Dry room (area included for all cell assembly steps), Plant area, m²": 61000.0,
            "Baseline Plant, Total formation process, Baseline Cell Capacity, Ah": 68.0,
            "Baseline Plant, Total formation process, Direct labor, hours/year": 560000.0,
            "Baseline Plant, Total formation process, Capital equipment, million$": 830.0,
            "Baseline Plant, Total formation process, Plant area, m²": 110000.0,
            "Baseline Plant, Module assembly, Direct labor, hours/year": 170000.0,
            "Baseline Plant, Module assembly, Capital equipment, million$": 94.0,
            "Baseline Plant, Module assembly, Plant area, m²": 27000.0,
            "Baseline Plant, Battery Pack Assembly and Testing, Number of modules per pack": 20.0,
            "Baseline Plant, Battery Pack Assembly and Testing, Direct labor, hours/year": 150000.0,
            "Baseline Plant, Battery Pack Assembly and Testing, Capital equipment, million$": 94.0,
            "Baseline Plant, Battery Pack Assembly and Testing, Plant area, m²": 27000.0,
            "Baseline Plant, Warehouse, Direct labor, hours/year": 31000.0,
            "Baseline Plant, Warehouse, Capital equipment, million$": 200.0,
            "Baseline Plant, Warehouse, Plant area, m²": 10000.0,
            "Baseline Plant, Building, Direct labor, hours/year": 0.0,
            "Baseline Plant, Building, Capital equipment, million$": 1700.0,
            "Baseline Plant, Building, Plant area, m²": 0.0,
            "Baseline Plant, Solvent recovery, Direct labor, hours/year": 17000.0,
            "Baseline Plant, Solvent recovery, Capital equipment, million$": 36.0,
            "Baseline Plant, Solvent recovery, Plant area, m²": 1100.0,
            "Baseline Plant, Rejected Cell and Scrap Recycle, Direct labor, hours/year": 38000.0,
            "Baseline Plant, Rejected Cell and Scrap Recycle, Capital equipment, million$": 9.3,
            "Baseline Plant, Rejected Cell and Scrap Recycle, Plant area, m²": 3300.0,
            "Baseline Plant, Control laboratory, Direct labor, hours/year": 46000.0,
            "Baseline Plant, Control laboratory, Capital equipment, million$": 16.0,
            "Baseline Plant, Control laboratory, Plant area, m²": 1300.0,
            "p, Materials preparation and delivery to coating, Positive materials, Direct labor, hours/year": 0.9,
            "p, Materials preparation and delivery to coating, Positive materials, Capital equipment, million$": 0.9,
            "p, Materials preparation and delivery to coating, Positive materials, Plant area, m²": 0.95,
            "p, Materials preparation and delivery to coating, Negative materials, Direct labor, hours/year": 0.9,
            "p, Materials preparation and delivery to coating, Negative materials, Capital equipment, million$": 0.9,
            "p, Materials preparation and delivery to coating, Negative materials, Plant area, m²": 0.95,
            "p, Electrode coating, Positive materials, Solvent evaporated, kg/m²yr": 0.2,
            "p, Electrode coating, Positive materials, Direct labor, hours/year": 0.7,
            "p, Electrode coating, Positive materials, Capital equipment, million$": 0.9,
            "p, Electrode coating, Positive materials, Plant area, m²": 0.95,
            "p, Electrode coating, Negative materials, Solvent evaporated, kg/m²yr": 0.2,
            "p, Electrode coating, Negative materials, Direct labor, hours/year": 0.7,
            "p, Electrode coating, Negative materials, Capital equipment, million$": 0.9,
            "p, Electrode coating, Negative materials, Plant area, m²": 0.95,
            "p, Calendering, Positive materials, Direct labor, hours/year": 0.7,
            "p, Calendering, Positive materials, Capital equipment, million$": 0.9,
            "p, Calendering, Positive materials, Plant area, m²": 0.95,
            "p, Calendering, Negative materials, Direct labor, hours/year": 0.7,
            "p, Calendering, Negative materials, Capital equipment, million$": 0.9,
            "p, Calendering, Negative materials, Plant area, m²": 0.95,
            "p, Notching, Positive materials, Direct labor, hours/year": 0.7,
            "p, Notching, Positive materials, Capital equipment, million$": 0.9,
            "p, Notching, Positive materials, Plant area, m²": 0.95,
            "p, Notching, Negative materials, Direct labor, hours/year": 0.7,
            "p, Notching, Negative materials, Capital equipment, million$": 0.9,
            "p, Notching, Negative materials, Plant area, m²": 0.95,
            "p, Vacuum Drying of Electrodes, Positive materials, Direct labor, hours/year": 0.7,
            "p, Vacuum Drying of Electrodes, Positive materials, Capital equipment, million$": 0.9,
            "p, Vacuum Drying of Electrodes, Positive materials, Plant area, m²": 0.95,
            "p, Vacuum Drying of Electrodes, Negative materials, Direct labor, hours/year": 0.7,
            "p, Vacuum Drying of Electrodes, Negative materials, Capital equipment, million$": 0.9,
            "p, Vacuum Drying of Electrodes, Negative materials, Plant area, m²": 0.95,
            "p, Electrode Slitting (positive and negative), Direct labor, hours/year": 0.7,
            "p, Electrode Slitting (positive and negative), Capital equipment, million$": 0.9,
            "p, Electrode Slitting (positive and negative), Plant area, m²": 0.95,
            "p, Cell stacking, Baseline Cell Capacity, Ah": 0.95,
            "p, Cell stacking, Direct labor, hours/year": 0.9,
            "p, Cell stacking, Capital equipment, million$": 0.9,
            "p, Cell stacking, Plant area, m²": 0.95,
            "p, Current collector welding, Direct labor, hours/year": 0.9,
            "p, Current collector welding, Capital equipment, million$": 0.9,
            "p, Current collector welding, Plant area, m²": 0.95,
            "p, X-ray inspection, Direct labor, hours/year": 0.9,
            "p, X-ray inspection, Capital equipment, million$": 0.9,
            "p, X-ray inspection, Plant area, m²": 0.95,
            "p, Inserting cell in container, Direct labor, hours/year": 0.9,
            "p, Inserting cell in container, Capital equipment, million$": 0.9,
            "p, Inserting cell in container, Plant area, m²": 0.95,
            "p, Electrolyte filling and cell sealing, Direct labor, hours/year": 0.9,
            "p, Electrolyte filling and cell sealing, Capital equipment, million$": 0.9,
            "p, Electrolyte filling and cell sealing, Plant area, m²": 0.95,
            "p, Dry room (area included for all cell assembly steps), Direct labor, hours/year": 0.0,
            "p, Dry room (area included for all cell assembly steps), Capital equipment, million$": 0.9,
            "p, Dry room (area included for all cell assembly steps), Plant area, m²": 0.95,
            "p, Total formation process, Baseline Cell Capacity, Ah": 0.3,
            "p, Total formation process, Direct labor, hours/year": 0.7,
            "p, Total formation process, Capital equipment, million$": 0.95,
            "p, Total formation process, Plant area, m²": 0.95,
            "p, Module assembly, Direct labor, hours/year": 0.7,
            "p, Module assembly, Capital equipment, million$": 0.95,
            "p, Module assembly, Plant area, m²": 0.95,
            "p, Battery Pack Assembly and Testing, Number of modules per pack": 0.3,
            "p, Battery Pack Assembly and Testing, Direct labor, hours/year": 0.7,
            "p, Battery Pack Assembly and Testing, Capital equipment, million$": 0.95,
            "p, Battery Pack Assembly and Testing, Plant area, m²": 0.95,
            "p, Warehouse, Direct labor, hours/year": 0.5,
            "p, Warehouse, Capital equipment, million$": 0.95,
            "p, Warehouse, Plant area, m²": 0.95,
            "p, Building, Direct labor, hours/year": 0.7,
            "p, Building, Capital equipment, million$": 0.95,
            "p, Building, Plant area, m²": 0.95,
            "p, Solvent recovery, Direct labor, hours/year": 0.5,
            "p, Solvent recovery, Capital equipment, million$": 0.95,
            "p, Solvent recovery, Plant area, m²": 0.95,
            "p, Rejected Cell and Scrap Recycle, Direct labor, hours/year": 0.7,
            "p, Rejected Cell and Scrap Recycle, Capital equipment, million$": 0.9,
            "p, Rejected Cell and Scrap Recycle, Plant area, m²": 0.95,
            "p, Control laboratory, Direct labor, hours/year": 0.7,
            "p, Control laboratory, Capital equipment, million$": 0.95,
            "p, Control laboratory, Plant area, m²": 0.95,
            "Baseline Manufacturing Rates, Effective full days of operation per year": 320.0,
            "Baseline Manufacturing Rates, Number of 8-hr shifts per day (2 for shipping and receiving)": 3.0,
            "Baseline Manufacturing Rates, Number of annual 8-h shifts": 960.0,
            "Baseline Manufacturing Rates, Energy, kWh per year": 49999999.999999985,
            "Baseline Manufacturing Rates, Number of battery packs manufactured per year": 500000.0,
            "Baseline Manufacturing Rates, Number of row racks per year": 2000000.0,
            "Baseline Manufacturing Rates, Number of modules per year": 10000000.0,
            "Baseline Manufacturing Rates, Number of cell interconnects per year": 270000000.0,
            "Baseline Manufacturing Rates, Number of accepted cells per year": 200000000.0,
            "Baseline Manufacturing Rates, Number of cells adjusted for yield": 211000000.0,
            "Baseline Manufacturing Rates, Positive electrode area, m² per year": 303000000.0,
            "Baseline Manufacturing Rates, Negative electrode area, m² per year": 315000000.0,
            "Baseline Manufacturing Rates, Positive active material, kg per year": 72500000.0,
            "Baseline Manufacturing Rates, Negative active material, kg per year": 49100000.0,
            "Baseline Manufacturing Rates, Positive binder solvent evaporated, kg per year": 24200000.0,
            "Baseline Manufacturing Rates, Negative binder solvent evaporated, kg per year": 40100000.0,
        },
        "Recycle": {
            "Elements 1": "Ni",
            "Elements 2": "Co",
            "Elements 3": "Mn",
            "Elements 4": "P",
        },
        "Thermal": {
            "Power for accessories (default = 0.5), kW": 0.5,
            "Power factor for rolling friction (default = 0.065), kW/mph": 0.065,
            "Power factor for aerodynamic drag (default = 4E-5, kW/(mph)³)": 4e-05,
            "Vehicle power efficiency factor (default = 0.833)": 0.833,
            # 'Designated constant speed at energy requirement, mph' : None,
            "Coolant heat capacity (default = 3.264), J/g-°C": 1.51,
            "Coolant density (ρ, default = 1.07), g/mL": 0.96,
            "Coolant viscosity (µ, default = 0.055), poise (g/s-cm)": 0.5,
            "Coolant conductivity (k), W/cm-°C": 0.00151,
            "Adequacy of Cooling,": 0.0,
            "Adequacy of Cooling, Excellent": 5.0,
            "Adequacy of Cooling, Good": 10.0,
            "Adequacy of Cooling, Fair": 15.0,
            "Adequacy of Cooling, Poor": 200.0,
            "Refrig 0, Cooling Capacity, W": 0.0,
            "Refrig 0, Added Mass, kg": 0.0,
            "Refrig 0, Added Volume, L": 0.0,
            "Refrig 0, Performance Coefficient": 0.0,
            "Refrig 0, Baseline Cost, $/pack": 0.0,
            "Refrig 1, Cooling Capacity, W": 500.0,
            "Refrig 1, Added Mass, kg": 2.0,
            "Refrig 1, Added Volume, L": 0.8,
            "Refrig 1, Performance Coefficient": 2.5,
            "Refrig 1, Baseline Cost, $/pack": 30.0,
            "Refrig 2, Cooling Capacity, W": 1000.0,
            "Refrig 2, Added Mass, kg": 3.0,
            "Refrig 2, Added Volume, L": 1.2,
            "Refrig 2, Performance Coefficient": 2.5,
            "Refrig 2, Baseline Cost, $/pack": 80.0,
            "Refrig 3, Cooling Capacity, W": 3000.0,
            "Refrig 3, Added Mass, kg": 5.0,
            "Refrig 3, Added Volume, L": 2.0,
            "Refrig 3, Performance Coefficient": 2.5,
            "Refrig 3, Baseline Cost, $/pack": 120.0,
            "Refrig 4, Cooling Capacity, W": 6000.0,
            "Refrig 4, Added Mass, kg": 7.0,
            "Refrig 4, Added Volume, L": 2.8,
            "Refrig 4, Performance Coefficient": 2.5,
            "Refrig 4, Baseline Cost, $/pack": 200.0,
        },
        "Tool-Generate Chem Couple": {
            "Select Method": "Create New Couple",
            "Positive, Select chemistries": "NMC811",
            "Negative, Select chemistries": "LTO",
            "Positive half-cell losses during formation, %": 0.05,
            "Negative half-cell losses during formation, %": 0.01,
            "Lithium inventory loss from SEI formation, mAh per g of negative": 20.0,
            "Negative half-cell cutoff voltage during formation, V vs. Li/Li+": 0.01,
            "Target N:P ratio after formation": 1.1,
            "Upper cutoff voltage at 100% SOC": 4.25,
            # 'SOC, 0' : None,
            # 'SOC, 10' : None,
            # 'SOC, 20' : None,
            # 'SOC, 30' : None,
            # 'SOC, 40' : None,
            # 'SOC, 50' : None,
            # 'SOC, 60' : None,
            # 'SOC, 70' : None,
            # 'SOC, 80' : None,
            # 'SOC, 90' : None,
            # 'SOC, 100' : None,
            "Chemistry Couple as Template": "NMC811-G (Power)",
            "New Couple Name": "NMC911",
        },
    }
    return properties


def test_function_is_version_compatible():
    version_to_compare = semantic_version.Version("5.4.3")

    self_version = semantic_version.Version("5.0.0")
    assert is_version_compatible(self_version, version_to_compare) == True

    with pytest.raises(ValueError):
        self_version = semantic_version.Version("100.0.0")
        assert is_version_compatible(self_version, version_to_compare)

    with pytest.raises(ValueError):
        self_version= semantic_version.Version("4.0.0")
        assert is_version_compatible(self_version, version_to_compare)

    with pytest.raises(ValueError):
        self_version = semantic_version.Version("5.100.0")
        assert is_version_compatible(self_version, version_to_compare, include_minor=True)


# Tests for battery class


@pytest.mark.parametrize(
    "battery_to_create, expected_battery_name",
    [
        ("Battery", "Battery"),
        ("Battery 2", "Battery 2"),
        ("NMC811 - G", "NMC811 - G"),
    ],
)
def test_create_battery_with_name(battery_to_create, expected_battery_name):
    test_battery = BatPaC_battery(battery_to_create)
    assert test_battery.name == expected_battery_name
    assert test_battery.properties == {}


def test_create_battery_without_name():
    test_battery = BatPaC_battery()
    assert test_battery.name == "Battery"
    assert test_battery.properties == {}


def test_load_battery_from_valid_file(example_battery_data):
    test_battery = BatPaC_battery("Battery 2")
    assert True == test_battery.load_battery_file(
        "./tests/test_batteries_config.toml", test_battery.name
    )
    properties = example_battery_data
    assert properties == test_battery.properties
    # print(example_battery_data )


def test_load_battery_from_invalid_file():
    test_battery = BatPaC_battery()
    assert False == test_battery.load_battery_file(
        "./tests/test_batteries_config.toml", test_battery.name
    )
    assert {} == test_battery.properties


def test_set_property(example_battery_data):
    test_battery = BatPaC_battery()
    test_battery.properties = example_battery_data
    assert test_battery.properties == example_battery_data
    test_battery.set_property("Dashboard", "Target rated peak power of pack, kW", 1)
    example_battery_data["Dashboard"]["Target rated peak power of pack, kW"] = 1
    assert test_battery.properties == example_battery_data


def test_set_new_property(example_battery_data):
    test_battery = BatPaC_battery()
    test_battery.set_new_property("new", "new", 1)
    test_property = {"new": {"new": 1}}
    assert test_battery.properties == test_property


def test_get_property():
    test_battery = BatPaC_battery()
    test_battery.set_new_property("new", "new", 1)
    test_property = {"new": {"new": 1}}
    assert test_battery.get_property("new", "new") == test_property["new"]["new"]


# Tests for BatPaC class
def test_create_batpac():
    test_batpac = BatPaC_tool(
        "./tests/test_batpac.xlsm",
        "./tests/test_BatPaC_user_input_cells.toml",
    )
    config = toml.load("./tests/test_BatPaC_user_input_cells.toml")
    config_metadata = config.pop("batpy")
    xw.books
    assert test_batpac.workbook_path == "./tests/test_batpac.xlsm"
    assert test_batpac.toml_path == "./tests/test_BatPaC_user_input_cells.toml"
    assert test_batpac.excel_cells == config
    assert test_batpac.batpac_version == config_metadata["BatPaC version"]
    assert test_batpac.batteries == []
    assert test_batpac.properties == {}
    # assert test_batpac.reset_macro == test_batpac.wb.macro("Module1.Reset")
    assert test_batpac.wb.fullname in [i.fullname for i in xw.books]
    # test_batpac.close()


def test_load_batpac(example_batpac_data):
    test_batpac = BatPaC_tool(
        "./tests/test_batpac.xlsm",
        "./tests/test_BatPaC_user_input_cells.toml",
    )
    test_batpac.load_batpac_file("./tests/test_batpac_config.toml")
    assert test_batpac.properties == example_batpac_data
    # test_batpac.close()


def test_add_battery():
    test_bat1 = BatPaC_battery("Battery 1")
    test_bat2 = BatPaC_battery("Battery 2")
    test_bat3 = BatPaC_battery("Battery 3")
    test_bat4 = BatPaC_battery("Battery 4")
    test_bat5 = BatPaC_battery("Battery 5")
    test_bat6 = BatPaC_battery("Battery 6")
    test_bat7 = BatPaC_battery("Battery 7")
    test_bat8 = BatPaC_battery("Battery 8")
    test_bat9 = BatPaC_battery("Battery 9")

    test_batpac = BatPaC_tool(
        "./tests/test_batpac.xlsm",
        "./tests/test_BatPaC_user_input_cells.toml",
    )

    test_batpac.add_battery(
        [test_bat1, test_bat2, test_bat3, test_bat4, test_bat5, test_bat6, test_bat7]
    )
    assert test_batpac.batteries == [
        test_bat1,
        test_bat2,
        test_bat3,
        test_bat4,
        test_bat5,
        test_bat6,
        test_bat7,
    ]

    test_batpac.add_battery(
        [
            test_bat8,
            test_bat9,
            test_bat3,
            test_bat4,
            test_bat5,
            test_bat6,
            test_bat7,
            test_bat1,
            test_bat2,
        ]
    )
    assert test_batpac.batteries != [
        test_bat8,
        test_bat9,
        test_bat3,
        test_bat4,
        test_bat5,
        test_bat6,
        test_bat7,
    ]
    test_batpac.batteries.clear()
    test_batpac.add_battery(
        [
            test_bat8,
            test_bat9,
            test_bat3,
            test_bat4,
            test_bat5,
            test_bat6,
            test_bat7,
            test_bat1,
            test_bat2,
        ]
    )
    assert test_batpac.batteries == [
        test_bat8,
        test_bat9,
        test_bat3,
        test_bat4,
        test_bat5,
        test_bat6,
        test_bat7,
    ]


def test_load_batteries_file(example_battery_data):
    test_batpac = BatPaC_tool(
        "./tests/test_batpac.xlsm",
        "./tests/test_BatPaC_user_input_cells.toml",
    )
    test_bat1 = BatPaC_battery("Battery 1")
    test_bat2 = BatPaC_battery("Battery 2")
    test_bat3 = BatPaC_battery("Battery 3")
    test_bat4 = BatPaC_battery("Battery 4")
    test_bat5 = BatPaC_battery("Battery 5")
    test_bat6 = BatPaC_battery("Battery 6")
    test_bat7 = BatPaC_battery("Battery 7")

    test_batpac.load_batteries_file(
        "./tests/test_batteries_config.toml",
        [test_bat1, test_bat2, test_bat3, test_bat4, test_bat5, test_bat6, test_bat7],
    )
    assert test_batpac.batteries[1].properties == example_battery_data


def test_write_read_value_direct():
    test_batpac = BatPaC_tool(
        "./tests/test_batpac.xlsm",
        "./tests/test_BatPaC_user_input_cells.toml",
    )
    test_batpac.write_value_direct("Dashboard", "A1", True)
    assert test_batpac.read_value_direct("Dashboard", "A1")
    test_batpac.write_value_direct("Dashboard", "A1", None)
    assert test_batpac.read_value_direct("Dashboard", "A1") == None
    with pytest.raises(KeyError):
        assert test_batpac.read_value_direct("no sheet", "no name")


def test_wb_helper_range():
    test_batpac = BatPaC_tool(
        "./tests/test_batpac.xlsm",
        "./tests/test_BatPaC_user_input_cells.toml",
    )
    test_bat1 = BatPaC_battery("Battery 1")
    test_batpac.add_battery([test_bat1])
    assert test_batpac.wb_helper_range("Dashboard", "Restart (0/1)") == "D6"
    assert (
        test_batpac.wb_helper_range(
            "Dashboard", "Target rated peak power of pack, kW", test_bat1
        )
        == "D38"
    )
    with pytest.raises(KeyError):
        assert test_batpac.wb_helper_range(
            "no sheet",
            "no name",
            battery=None,
            additional_cell_config="./tests/test_BatPaC_calculation_and_validation_results.toml",
        )


def test_write_read_value():
    test_batpac = BatPaC_tool(
        "./tests/test_batpac.xlsm",
        "./tests/test_BatPaC_user_input_cells.toml",
    )
    test_bat1 = BatPaC_battery("Battery 1")
    test_batpac.add_battery([test_bat1])

    test_batpac.write_value("Dashboard", "Restart (0/1)", 0)
    assert test_batpac.read_value("Dashboard", "Restart (0/1)") == 0

    test_batpac.write_value_battery(
        "Dashboard", "Target rated peak power of pack, kW", test_bat1, True
    )
    assert test_batpac.read_value_battery(
        "Dashboard", "Target rated peak power of pack, kW", test_bat1
    )

    test_batpac.write_value_battery(
        "Dashboard", "Target rated peak power of pack, kW", test_bat1, 100
    )
    assert (
        test_batpac.read_value_battery(
            "Dashboard", "Target rated peak power of pack, kW", test_bat1
        )
        == 100
    )
    with pytest.raises(KeyError):
        assert test_batpac.read_value("no sheet", "no name", {})

    test_batpac.write_value("Dashboard", "Restart (0/1)", 1)
    assert test_batpac.read_value("Dashboard", "Restart (0/1)") == 1


def test_stop_automatic_calculation():
    test_batpac = BatPaC_tool(
        "./tests/test_batpac.xlsm",
        "./tests/test_BatPaC_user_input_cells.toml",
    )
    test_batpac.stop_automatic_calculation()
    assert test_batpac.read_value("Dashboard", "Restart (0/1)") == 0


def test_is_version_compatible():
    test_batpac = BatPaC_tool(
        "./tests/test_batpac.xlsm",
        "./tests/test_BatPaC_user_input_cells.toml",
    )
    version_to_compare = semantic_version.Version("5.4.3")

    test_batpac.version = semantic_version.Version("5.0.0")
    assert test_batpac.is_version_compatible(version_to_compare) == True

    with pytest.raises(ValueError):
        test_batpac.version = semantic_version.Version("100.0.0")
        assert test_batpac.is_version_compatible(version_to_compare)

    with pytest.raises(ValueError):
        test_batpac.version = semantic_version.Version("4.0.0")
        assert test_batpac.is_version_compatible(version_to_compare)

    with pytest.raises(ValueError):
        test_batpac.version = semantic_version.Version("5.100.0")
        assert test_batpac.is_version_compatible(version_to_compare, include_minor=True)


def test_start_automatic_calculation():
    test_batpac = BatPaC_tool(
        "./tests/test_batpac.xlsm",
        "./tests/test_BatPaC_user_input_cells.toml",
    )
    test_batpac.start_automatic_calculation()
    assert test_batpac.read_value("Dashboard", "Restart (0/1)") == 1


def test_calculate():
    test_batpac = BatPaC_tool(
        "./tests/test_batpac.xlsm",
        "./tests/test_BatPaC_user_input_cells.toml",
    )
    test_bat1 = BatPaC_battery("Battery 1")
    test_bat2 = BatPaC_battery("Battery 2")
    test_bat3 = BatPaC_battery("Battery 3")
    test_bat4 = BatPaC_battery("Battery 4")
    test_bat5 = BatPaC_battery("Battery 5")
    test_bat6 = BatPaC_battery("Battery 6")
    test_bat7 = BatPaC_battery("Battery 7")

    test_batpac.load_batteries_file(
        "./tests/test_batteries_config.toml",
        [test_bat1, test_bat2, test_bat3, test_bat4, test_bat5, test_bat6, test_bat7],
    )
    test_batpac.load_batpac_file("./tests/test_batpac_config.toml")
    test_batpac.calculate()
    for sheet in test_batpac.batteries[0].properties:
        for key, value in test_batpac.batteries[0].properties[sheet].items():
            assert test_batpac.read_value_battery(sheet, key, test_bat1) == value


def test_save_config(example_battery_data):
    test_batpac = BatPaC_tool(
        "./tests/test_batpac.xlsm",
        "./tests/test_BatPaC_user_input_cells.toml",
    )
    test_bat1 = BatPaC_battery("Battery 1")
    test_bat2 = BatPaC_battery("Battery 2")
    test_bat3 = BatPaC_battery("Battery 3")
    test_bat4 = BatPaC_battery("Battery 4")
    test_bat5 = BatPaC_battery("Battery 5")
    test_bat6 = BatPaC_battery("Battery 6")
    test_bat7 = BatPaC_battery("Battery 7")

    test_batpac.add_battery(
        [test_bat1, test_bat2, test_bat3, test_bat4, test_bat5, test_bat6, test_bat7],
    )
    assert test_batpac.properties == {}
    for battery in test_batpac.batteries:
        assert battery.properties == {}

    assert True == test_bat2.load_battery_file(
        "./tests/test_batteries_config.toml", test_bat2.name
    )
    properties = example_battery_data
    assert properties == test_bat2.properties
    test_batpac.calculate()
    test_batpac.batteries[5].set_new_property("new", "new", "new")
    test_batpac.save_config()
    assert test_batpac.properties != {}
    for battery in test_batpac.batteries:
        assert battery.properties != {}
        if battery.name == "Battery 2":
            assert battery.properties == example_battery_data

    path_saved_batpac = pathlib.Path("./tests/saved_test_batpac_config.toml")
    assert path_saved_batpac.is_file() == False

    path_saved_batteries = pathlib.Path("./tests/saved_test_batteries_config.toml")
    assert path_saved_batteries.is_file() == False

    test_batpac.save_config(path_saved_batpac, path_saved_batteries)
    assert test_batpac.properties != {}
    for battery in test_batpac.batteries:
        assert battery.properties != {}
        if battery.name == "Battery 2":
            assert battery.properties == example_battery_data

    assert path_saved_batpac.is_file()
    assert path_saved_batteries.is_file()

    pathlib.Path.unlink(path_saved_batpac)
    pathlib.Path.unlink(path_saved_batteries)


def test_from_user_input():
    assert True


def test_read_calculation_and_validation_results():
    test_batpac = BatPaC_tool(
        "./tests/test_batpac.xlsm",
        "./tests/test_BatPaC_user_input_cells.toml",
        "./tests/test_BatPaC_calculation_and_validation_results.toml",
    )
    test_bat1 = BatPaC_battery("Battery 1")
    test_bat2 = BatPaC_battery("Battery 2")
    test_bat3 = BatPaC_battery("Battery 3")
    test_bat4 = BatPaC_battery("Battery 4")
    test_bat5 = BatPaC_battery("Battery 5")
    test_bat6 = BatPaC_battery("Battery 6")
    test_bat7 = BatPaC_battery("Battery 7")

    test_batpac.load_batteries_file(
        "./tests/test_batteries_config.toml",
        [test_bat1, test_bat2, test_bat3, test_bat4, test_bat5, test_bat6, test_bat7],
    )
    test_batpac.load_batpac_file("./tests/test_batpac_config.toml")
    test_batpac.calculate()

    validation_1 = test_batpac.read_calculation_and_validation_results()
    assert validation_1 != {}

    test_batpac.toml_calculation_validation_results_path = None
    validation_2 = test_batpac.read_calculation_and_validation_results()
    assert validation_2 == False

    validation_3 = test_batpac.read_calculation_and_validation_results(
        "./tests/test_BatPaC_calculation_and_validation_results.toml"
    )
    assert validation_3 != {}
    assert validation_1 == validation_3


def test_save():
    test_batpac = BatPaC_tool(
        "./tests/test_batpac.xlsm",
        "./tests/test_BatPaC_user_input_cells.toml",
    )
    path_saved_batpac = pathlib.Path("./tests/saved_test_batpac.xlsm")
    assert path_saved_batpac.is_file() == False

    test_batpac.save(path_saved_batpac)
    assert path_saved_batpac.is_file()

    test_batpac.close()
    pathlib.Path.unlink(path_saved_batpac)

    test_batpac = BatPaC_tool(
        "./tests/test_batpac.xlsm",
        "./tests/test_BatPaC_user_input_cells.toml",
    )
    path_saved_batpac = pathlib.Path(test_batpac.workbook_path)
    test_batpac.save()
    assert path_saved_batpac.is_file()
    test_batpac.close()


def test_close_batpac():
    test_batpac = BatPaC_tool(
        "./tests/test_batpac.xlsm",
        "./tests/test_BatPaC_user_input_cells.toml",
    )
    assert test_batpac.close()

    test_batpac = BatPaC_tool(
        "./tests/test_batpac.xlsm",
        "./tests/test_BatPaC_user_input_cells.toml",
    )
    test_batpac.wb.close()
    del test_batpac

    test_batpac = BatPaC_tool(
        "./tests/test_batpac.xlsm",
        "./tests/test_BatPaC_user_input_cells.toml",
    )
    xw.Book()
    assert test_batpac.close()
    # new_book.app.quit()
    for app in xw.apps:
        app.quit()
