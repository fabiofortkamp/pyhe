import pytest
from pyhe import SimpleRankineCycle, CarnotSteadyStateCycle
from CoolProp.CoolProp import PropsSI

def test_calculate_efficiency_returns_positive():

    P_condenser = 10e3
    P_boiler = 100e3
    src = SimpleRankineCycle(P_condenser,P_boiler)
    src.run()

    eta = src.metrics["Thermal efficiency"]

    assert eta >= 0

def test_calculate_efficiency_returns_below_Carnot():
    
    P_condenser = 10e3
    P_boiler = 100e3
    src = SimpleRankineCycle(P_condenser,P_boiler)
    src.run()

    eta = src.metrics["Thermal efficiency"]

    T_L = PropsSI("T","P",P_condenser,"Q",0,"Water")
    T_H = PropsSI("T","P",P_boiler,"Q",0,"Water")
    Delta_s = 1

    cm = CarnotSteadyStateCycle(T_L,T_H,Delta_s)
    cm.run()
    eta_carnot = cm.metrics["Thermal efficiency"]

    assert eta < eta_carnot

def test_calculate_specific_work_returns_positive():

    P_condenser = 10e3
    P_boiler = 100e3
    src = SimpleRankineCycle(P_condenser,P_boiler)
    src.run()

    w = src.metrics["Specific work"]

    assert w >= 0
    
def test_negative_P_condenser_raises_exception():
    
    with pytest.raises(ValueError) as excinfo:
        src = SimpleRankineCycle(-1,10)
    
    exception_msg = excinfo.value.args[0]
    assert exception_msg == "Pressure values cannot be negative."

def test_negative_P_boiler_raises_exception():
    
    with pytest.raises(ValueError) as excinfo:
        src = SimpleRankineCycle(1,-10)
    
    exception_msg = excinfo.value.args[0]
    assert exception_msg == "Pressure values cannot be negative."

def test_ordering_pressures():
    
    with pytest.raises(ValueError) as excinfo:
        src = SimpleRankineCycle(1e3,1e2)

    exception_msg = excinfo.value.args[0]
    assert exception_msg == "Condenser pressure should be lower than boiler pressure."