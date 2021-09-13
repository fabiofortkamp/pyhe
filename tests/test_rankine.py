import pytest
from pyhe import SimpleRankineCycle, CarnotSteadyStateCycle
from CoolProp.CoolProp import PropsSI

# These tests currently only apply to water as the working fluid.

@pytest.mark.parametrize(
    "P_condenser,P_boiler",
   [
      (5e3,1e6),
      (10e3,16e6),
      (15e3,20e6),
      (15e3,500e3) 
   ] 
)
def test_calculate_efficiency_returns_positive(P_condenser,P_boiler):


    src = SimpleRankineCycle(P_condenser,P_boiler)
    src.run()

    eta = src.metrics["Thermal efficiency"]

    assert eta >= 0

@pytest.mark.parametrize(
    "P_condenser,P_boiler",
   [
      (5e3,1e6),
      (10e3,16e6),
      (15e3,20e6),
      (15e3,500e3) 
   ] 
)
def test_calculate_efficiency_returns_below_Carnot(P_condenser,P_boiler):
    
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


@pytest.mark.parametrize(
    "P_condenser,P_boiler",
   [
      (5e3,1e6),
      (10e3,16e6),
      (15e3,20e6),
      (15e3,500e3) 
   ] 
)
def test_calculate_specific_work_returns_positive(P_condenser,P_boiler):

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

@pytest.mark.parametrize(
    "P_condenser,P_boiler",
   [
      (5e3,1e6),
      (10e3,16e6),
      (15e3,20e6),
      (15e3,500e3) 
   ] 
)
def test_Simple_Rankine_cycle_obeys_First_Law(P_condenser,P_boiler):
    src = SimpleRankineCycle(P_condenser,P_boiler)
    src.run()

    wturbine = src.metrics["Turbine work"]
    wpump = src.metrics["Pump work"]
    qboiler = src.metrics["Boiler heat"]
    qcondenser = src.metrics["Condenser heat"]

    residual = (qboiler + wpump) - (wturbine + qcondenser)
    assert residual >= 0