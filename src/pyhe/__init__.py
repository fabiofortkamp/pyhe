from collections import namedtuple
from operator import index
import math

from CoolProp.CoolProp import PropsSI
import numpy as np
from numpy.core.function_base import add_newdoc
from scipy.interpolate import interp1d
from scipy.optimize import fsolve
from pandas import DataFrame,read_csv

import pathlib

here = pathlib.Path(__file__).parent.resolve()

class CarnotSteadyStateCycle(object):

    
    def __init__(self, T_L,T_H,Delta_s):
        """Carnot cycle in steady state form.

        Args:
            T_L : low side temperature [K]
            T_H : hot side temperature [K]
            Delta_s : specific entropy change [J/(kg K)]
        """

        self.validate_args(T_L,T_H,Delta_s)
        self.T_H = T_H
        self.T_L = T_L
        self.Delta_s = Delta_s
        self.metrics = {
            "Thermal efficiency": None,
            "Specific work": None,
            "Input heat": None,
            "Output heat":None
            
        }

    def validate_args(self,T_L,T_H,Delta_s):

        if T_L < 0:
            raise ValueError("Temperature values cannot be negative.")

        if T_H < 0:
            raise ValueError("Temperature values cannot be negative.")

        if T_L > T_H:
            raise ValueError("The cold-side temperature should be smaller than the hot side value.")

        if Delta_s < 0:
            raise ValueError("Entropy variation should be positive.")

    def run(self):
        """Run the Carnot cycle model and update the 'metrics' attribute.

        Keys:

        "Thermal efficiency": ratio of specific work to input heat, from 0 to 1
        "Specific work": the net output work, in [J/kg]
        "Input heat": in [J/kg]
        "Output heat": in [J/kg]

        """

        self.metrics = {
            "Thermal efficiency": 1 - self.T_L/self.T_H,
            "Specific work": (self.T_H - self.T_L)*self.Delta_s,
            "Input heat": (self.T_H*self.Delta_s),
            "Output heat": (self.T_L*self.Delta_s)
            
        }

class SimpleRankineCycle(object):
    
    def __init__(self, P_condenser, P_boiler,fluid='Water'):
        """Simple Rankine (no superheat) cycle in steady state form.

        The cycle is ideal: pump and turbine are isentropic, there are no 
        pressure drops in heat exchangers, and no variations of 
        kinetic and potential energy

        Args:
            P_condenser : condenser pressure [Pa]
            P_boiler : boiler pressure [Pa]
            fluid : working fluid, should be included in:
            http://www.coolprop.org/fluid_properties/PurePseudoPure.html#list-of-fluids 
        """

        self.validate_args(P_condenser,P_boiler)
        self.P_condenser = P_condenser
        self.P_boiler = P_boiler
        self.fluid = fluid
        self.metrics = {
            "Thermal efficiency": None,
            "Specific work": None,
            "Temperatures": None,
            "Entropy values": None,
            "Boiler heat": None,
            "Condenser heat": None,
            "Pump work": None,
            "Turbine work": None,
        }

    def validate_args(self,P_condenser,P_boiler):
    
        if P_condenser < 0:
            raise ValueError("Pressure values cannot be negative.")

        if P_boiler < 0:
            raise ValueError("Pressure values cannot be negative.")

        if P_boiler < P_condenser:
            raise ValueError("Condenser pressure should be lower than boiler pressure.")

    def run(self):

        """Run the Simple Rankine cycle model and update the 'metrics' attribute.

        In the array attributes, the order of states is:

        0: pump inlet or condenser outlet
        1: pump outlet or boiler inlet
        2: boiler outlet or turbine inlet
        3: turbine outlet or condenser inlet

        Keys:

        "Thermal efficiency": ratio of specific work to input heat, from 0 to 1
        "Specific work": the net output work, in [J/kg]
        "Temperatures": array of temperatures (see above) in [K]
        "Entropy values": array of specific entropy (see above) in [J/(kg K)]
        "Boiler heat": in [J/kg]
        "Condenser heat": in [J/kg]
        "Pump work": in [J/kg]
        "Turbine work": in [J/kg]

        """

        P_condenser = self.P_condenser
        P_boiler = self.P_boiler
        fluid = self.fluid
        h1 = PropsSI("H","P",P_condenser,"Q",0,fluid)
        s1 = PropsSI("S","P",P_condenser,"Q",0,fluid)
        T1 = PropsSI("T","P",P_condenser,"Q",0,fluid)

        # CoolProp has no specific volume
        # we calculate the density and take the inverse
        v1 = (PropsSI("D","P",P_condenser,"Q",0,fluid))**(-1)

        # assuming incompressible liquid, no variations of 
        # kinetic and potential energy
        w_pump = v1 * (P_boiler - P_condenser)

        # First Law Analysis in Pump
        h2 = h1 + w_pump

        # Second Law Analysis in Pump
        s2 = s1
        T2 = PropsSI("T","H",h2,"S",s2,fluid)

        h3 = PropsSI("H","P",P_boiler,"Q",1,fluid)
        s3 = PropsSI("S","P",P_boiler,"Q",1,fluid)
        T3 = PropsSI("T","P",P_boiler,"Q",1,fluid)

        # First Law Analysis in Boiler
        q_boiler = h3 - h2

        # Second Law Analysis in Turbine
        s4 = s3
        T4 = T1
        h4 = PropsSI("H","P",P_condenser,"S",s4,fluid)

        # First Law Analysis in Turbine
        w_turbine = h3 - h4

        # First Law Analysis in Condenser
        q_condenser = h4 - h1

        w_net = w_turbine - w_pump

        # thermal efficiency
        eta_t = w_net/q_boiler

        self.metrics = {
            "Thermal efficiency": eta_t,
            "Specific work": w_net,
            "Temperatures": np.array([T1,T2,T3,T4]),
            "Entropy values": np.array([s1,s2,s3,s4]),
            "Boiler heat": q_boiler,
            "Condenser heat": q_condenser,
            "Pump work": w_pump,
            "Turbine work": w_turbine,
        }

class RankineWithSuperheatCycle(object):
    
    def __init__(self, P_condenser, P_boiler,T_turbine_inlet,fluid='Water'):
        """Rankine (with superheat) cycle in steady state form.

        The cycle is ideal: pump and turbine are isentropic, there are no 
        pressure drops in heat exchangers, and no variations of 
        kinetic and potential energy

        Args:
            P_condenser : condenser pressure [Pa]
            P_boiler : boiler pressure [Pa]
            T_turbine_inlet: inlet turbine temperature [K]
            fluid : working fluid, should be included in:
            http://www.coolprop.org/fluid_properties/PurePseudoPure.html#list-of-fluids 
        """

        self.validate_args(P_condenser,P_boiler,T_turbine_inlet,fluid)
        self.P_condenser = P_condenser
        self.P_boiler = P_boiler
        self.T_turbine_inlet = T_turbine_inlet
        self.fluid = fluid
        self.metrics = {
            "Thermal efficiency": None,
            "Specific work": None,
            "Temperatures": None,
            "Entropy values": None,
            "Boiler heat": None,
            "Superheater heat": None,
            "Condenser heat": None,
            "Pump work": None,
            "Turbine work": None,
        }

    def validate_args(self,P_condenser,P_boiler,T_turbine_inlet,fluid):
    
        if P_condenser < 0:
            raise ValueError("Pressure values cannot be negative.")

        if P_boiler < 0:
            raise ValueError("Pressure values cannot be negative.")

        if P_boiler < P_condenser:
            raise ValueError("Condenser pressure should be lower than boiler pressure.")

        if T_turbine_inlet <= PropsSI("T","P",P_boiler,"Q",1,fluid):
            raise ValueError("Turbine inlet temperature should be above saturation temperature at boiler pressure")

    def run(self):

        """Run the Simple Rankine cycle model and update the 'metrics' attribute.

        In the array attributes, the order of states is:

        0: pump inlet or condenser outlet
        1: pump outlet or boiler inlet
        2: boiler outlet or superheater inlet
        3: superheater outlet or turbine inlet 
        4: turbine outlet or condenser inlet

        Keys:

        "Thermal efficiency": ratio of specific work to input heat, from 0 to 1
        "Specific work": the net output work, in [J/kg]
        "Temperatures": array of temperatures (see above) in [K]
        "Entropy values": array of specific entropy (see above) in [J/(kg K)]
        "Boiler heat": in [J/kg]
        "Superheater heat": in [J/kg]
        "Condenser heat": in [J/kg]
        "Pump work": in [J/kg]
        "Turbine work": in [J/kg]

        """

        P_condenser = self.P_condenser
        P_boiler = self.P_boiler
        fluid = self.fluid
        h1 = PropsSI("H","P",P_condenser,"Q",0,fluid)
        s1 = PropsSI("S","P",P_condenser,"Q",0,fluid)
        T1 = PropsSI("T","P",P_condenser,"Q",0,fluid)

        # CoolProp has no specific volume
        # we calculate the density and take the inverse
        v1 = (PropsSI("D","P",P_condenser,"Q",0,fluid))**(-1)

        # assuming incompressible liquid, no variations of 
        # kinetic and potential energy
        w_pump = v1 * (P_boiler - P_condenser)

        # First Law Analysis in Pump
        h2 = h1 + w_pump

        # Second Law Analysis in Pump
        s2 = s1
        T2 = PropsSI("T","H",h2,"S",s2,fluid)

        h3 = PropsSI("H","P",P_boiler,"Q",1,fluid)
        s3 = PropsSI("S","P",P_boiler,"Q",1,fluid)
        T3 = PropsSI("T","P",P_boiler,"Q",1,fluid)

        # First Law Analysis in Boiler
        q_boiler = h3 - h2

        T4 = self.T_turbine_inlet
        h4 = PropsSI("H","P",P_boiler,"T",T4,fluid)
        s4 = PropsSI("S","P",P_boiler,"T",T4,fluid)

        # First Law Analysis in Superheater
        q_superheater = h4 - h3

        # Second Law Analysis in Turbine
        s5 = s4
        T5 = T1
        h5 = PropsSI("H","P",P_condenser,"S",s5,fluid)

        # First Law Analysis in Turbine
        w_turbine = h4 - h5

        # First Law Analysis in Condenser
        q_condenser = h5 - h1

        w_net = w_turbine - w_pump

        # thermal efficiency
        eta_t = w_net/(q_boiler+q_superheater)

        self.metrics = {
            "Thermal efficiency": eta_t,
            "Specific work": w_net,
            "Temperatures": np.array([T1,T2,T3,T4,T5]),
            "Entropy values": np.array([s1,s2,s3,s4,s5]),
            "Boiler heat": q_boiler,
            "Condenser heat": q_condenser,
            "Superheater heat": q_superheater,
            "Pump work": w_pump,
            "Turbine work": w_turbine,
        }

HF_TABLE_FILE = here / "hformation.csv"
HF_INDEX_LABEL = "Substance"
HF_FORMULA_LABEL = "Formula"
HF_MOLAR_MASSS_LABEL = "M(kg/kmol)"
HF_FORMATION_ENTHALPY_LABEL = "Enthalpy of formation(kJ/kmol)"
HF_GIBBS_FUNCTION_LABEL = "Gibbs function of formation (kJ/kmol)"
HF_ABSOLUTE_ENTROPY_LABEL = "Absolute entropy (kJ/kmolK)"
HF_HHV_LABEL = "HHV(kJ/kg)"
HF_LHV_LABEL = "LHV(kJ/kg)"
HF_DF = read_csv(
    HF_TABLE_FILE,
    index_col=0,
    )

STANDARD_TEMPERATURE = 298
STANDARD_PRESSURE_ATM = 1

GI_TABLE_FILE = here / "gasideal.csv"
GI_PREAMBLE_NUMBER_OF_LINES = 6
GI_HEADER_LINE = 7

GI_TEMPERATURE_COLUMN = 0
GI_NUMBER_OF_PROPERTIES = 3
GI_PROPERTIES = [
    "H",
    "U",
    "S"
]
GI_FLUIDS = [
    "Carbon dioxide",
    "Carbon monoxide",
    "Steam",
    "Oxygen gas",
    "Nitrogen gas"]

UNIVERSAL_GAS_CONSTANT = 8.31447
NITROGEN_AIR_MOLAR_FRACTION = 0.79
OXYGEN_AIR_MOLAR_FRACTION = 0.21

def _get_column_number_for_ideal_gas_table(fluid,property):
    "Return the index of the column to be read to yield the property of fluid."

    ifluid = GI_FLUIDS.index(fluid)
    ip = GI_PROPERTIES.index(property)

    N = len(GI_PROPERTIES)

    return 1 + N*ifluid + ip

def _calculate_ideal_gas_property(fluid,property,T):
    "Return an interpolated value of property(fluid,T)"

    # this is highly inefficient
    
    M = np.loadtxt(GI_TABLE_FILE,delimiter=",",skiprows=GI_HEADER_LINE)
    
    x = M[:,GI_TEMPERATURE_COLUMN]
    y = M[:,_get_column_number_for_ideal_gas_table(fluid,property)]

    return np.interp(T,x,y)

def ideal_gas_enthalpy(fluid,T):
    "Return the ideal gas enthalpy in kJ/kmol"
    return 1e3*_calculate_ideal_gas_property(fluid,'H',T)

def ideal_gas_absolute_entropy(fluid,T):
    "Return the ideal gas absolute entropy in kJ/(kmol K)"
    return _calculate_ideal_gas_property(fluid,'S',T)
  

def enthalpy_of_formation(fluid):
    "Return the molar enthalpy of formation in kJ/kmol"

    return HF_DF.loc[fluid][HF_FORMATION_ENTHALPY_LABEL]

def standard_absolute_entropy(fluid):
    "Return the standard absolute  molar entropy kJ/(kmol K)"

    return HF_DF.loc[fluid][HF_ABSOLUTE_ENTROPY_LABEL]

def molar_mass(fluid):
    "Return the molar mass in kg/kmol"

    return HF_DF.loc[fluid][HF_MOLAR_MASSS_LABEL]
