import pytest
from pyhe import CarnotSteadyStateCycle

def test_calculate_efficiency():

    T_L = 100
    T_H = 200
    Delta_s = 0.1
    cm = CarnotSteadyStateCycle(T_L,T_H,Delta_s)
    cm.run()

    eta = cm.metrics["Thermal efficiency"]

    eta_Carnot = 1 - T_L/T_H

    assert eta == eta_Carnot

def test_calculate_specific_work():

    T_L = 340
    T_H = 400

    Delta_s = 0.7

    cm = CarnotSteadyStateCycle(T_L,T_H,Delta_s)
    cm.run()

    specific_work = cm.metrics["Specific work"]

    w = (T_H - T_L)*Delta_s

    assert specific_work == w
    
# temperatures should be positive
def test_negative_T_H_raises_exception():
    
    with pytest.raises(ValueError) as excinfo:
        cm = CarnotSteadyStateCycle(200,-400,0.3)
    
    exception_msg = excinfo.value.args[0]
    assert exception_msg == "Temperature values cannot be negative."

def test_negative_T_L_raises_exception():
    
    with pytest.raises(ValueError) as excinfo:
        cm = CarnotSteadyStateCycle(-200,400,0.3)
    
    exception_msg = excinfo.value.args[0]
    assert exception_msg == "Temperature values cannot be negative."

def test_negative_Delta_s_raises_exception():
    
    with pytest.raises(ValueError) as excinfo:
        cm = CarnotSteadyStateCycle(200,400,-0.3)
    
    exception_msg = excinfo.value.args[0]
    assert exception_msg == "Entropy variation should be positive."

# should not work if T_L > T_H
def test_ordering_temperatures():
    
    with pytest.raises(ValueError) as excinfo:
        cm = CarnotSteadyStateCycle(400,200,0.5)

    exception_msg = excinfo.value.args[0]
    assert exception_msg == "The cold-side temperature should be smaller than the hot side value."

# efficiency, power should be zero if T_L = T_H

