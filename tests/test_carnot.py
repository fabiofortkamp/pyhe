import pytest
from pyhe import CarnotSteadyStateCycle

@pytest.mark.parametrize(
    "T_L,T_H,Delta_s",
    [
        (100,200,1),
        (0,100,1),
        (300,100000000000000,0.1),
        (0,10000000000000000,1),
        (200,400,0.5),
        (1000,200000,4)
    ]
)
def test_calculate_efficiency(T_L,T_H,Delta_s):


    cm = CarnotSteadyStateCycle(T_L,T_H,Delta_s)
    cm.run()

    eta = cm.metrics["Thermal efficiency"]

    eta_Carnot = 1 - T_L/T_H

    assert eta == eta_Carnot


@pytest.mark.parametrize(
    "T_L,T_H,Delta_s",
    [
        (100,200,1),
        (0,100,1),
        (300,100000000000000,0.1),
        (0,10000000000000000,1),
        (200,400,0.5),
        (1000,200000,4)
    ]
)
def test_calculate_specific_work(T_L,T_H,Delta_s):

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
@pytest.mark.parametrize("T_L",[200,500,1000])
def test_power_zero_if_temperaturas_equal(T_L):
    Delta_s = 1
    T_H = T_L

    cm = CarnotSteadyStateCycle(T_L,T_H,Delta_s)
    cm.run()

    specific_work = cm.metrics["Specific work"]
    assert specific_work == 0

@pytest.mark.parametrize("T_L",[200,500,1000])
def test_efficiency_zero_if_temperaturas_equal(T_L):
    Delta_s = 1
    T_H = T_L

    cm = CarnotSteadyStateCycle(T_L,T_H,Delta_s)
    cm.run()

    eta = cm.metrics["Thermal efficiency"]
    assert eta == 0

@pytest.mark.parametrize(
    "T_L,T_H,Delta_s",
    [
        (100,200,1),
        (0,100,1),
        (300,100000000000000,0.1),
        (0,10000000000000000,1),
        (200,400,0.5),
        (1000,200000,4)
    ]
)
def test_Carnot_cycle_obey_First_Law(T_L,T_H,Delta_s,):
    cm = CarnotSteadyStateCycle(T_L,T_H,Delta_s)
    cm.run()

    w = cm.metrics["Specific work"]
    qin = cm.metrics["Input heat"]
    qout = cm.metrics["Output heat"]

    assert (qin - w - qout) == 0
