from collections import namedtuple


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

class RankineCycle(object):
    
    def __init__(self, P_condenser, P_boiler):
        pass