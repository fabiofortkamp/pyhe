from collections import namedtuple
from CoolProp.CoolProp import PropsSI
import numpy as np

class CarnotSteadyStateCycle(object):

    
    def __init__(self, T_L,T_H,Delta_s):
        """Carnot cycle in steady state form.

        Args:
            T_L : low side temperature [K]
            T_H : hot side temperature [K]
            Delta_s : specific entropy change [kJ/(kg K)]
        """

        self.validate_args(T_L,T_H,Delta_s)
        self.T_H = T_H
        self.T_L = T_L
        self.Delta_s = Delta_s
        self.metrics = {
            "Thermal efficiency": None,
            "Specific work": None
            
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
        """Run the Carnot cycle model and update its metrics

        """

        self.metrics = {
            "Thermal efficiency": 1 - self.T_L/self.T_H,
            "Specific work": (self.T_H - self.T_L)*self.Delta_s
            
        }

class SimpleRankineCycle(object):
    
    def __init__(self, P_condenser, P_boiler,fluid='Water'):

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

        P_condenser = self.P_condenser
        P_boiler = self.P_boiler
        fluid = self.fluid
        h1 = PropsSI("H","P",P_condenser,"Q",0,fluid)
        s1 = PropsSI("S","P",P_condenser,"Q",0,fluid)
        T1 = PropsSI("T","P",P_condenser,"Q",0,fluid)

        # CoolProp has no specific volume
        # we calculate the density and take the inverse
        v1 = (PropsSI("D","P",P_condenser,"Q",0,fluid))**(-1)

        w_pump = v1 * (P_boiler - P_condenser)

        h2 = h1 + w_pump
        s2 = s1
        T2 = PropsSI("T","H",h2,"S",s2,fluid)

        h3 = PropsSI("H","P",P_boiler,"Q",1,fluid)
        s3 = PropsSI("S","P",P_boiler,"Q",1,fluid)
        T3 = PropsSI("T","P",P_boiler,"Q",1,fluid)

        q_boiler = h3 - h2

        s4 = s3
        T4 = T1
        h4 = PropsSI("H","P",P_condenser,"S",s4,fluid)

        w_turbine = h3 - h4
        q_condenser = h4 - h1

        w_net = w_turbine - w_pump

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





