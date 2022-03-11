# pyhe - Python models for Heat Engines

This project simulates simplified model for Heat Engines. It is mainly used as for teaching purposes.

## Usage

```python
import pyhe

T_L = 200
T_H = 400
Delta_s = 500
cm = pyhe.CarnotSteadyStateCycle(T_L,T_H,Delta_s)
cm.run()
eta_t = cm.metrics["Thermal efficiency"]
w = cm.metrics["Specific work"]

fluid = 'Carbon dioxide'
hfo = pyhe.enthalpy_of_formation(fluid)
T = 434
s = pyhe.absolute_ideal_gas_entropy(fluid,T)
```

## Installation

This package is installable with

```shell
    pip install .
```

To develop"

```shell
    pip install .[dev,test]
```

See `requirements.txt` and `requirements-dev.txt` for the environment requirements.

## Testing

Tests are available with `pytest`.

The tests currently check for some basic conditions, like exception when certain parameters are not valid, and also for validity of the First and Second Law of Thermodynamics. For the combustion functions, the tests assert that valid values are returned (such as negative enthalpy of formation for exotermic reactions) and that all functions can be accessed.

Notice that currently tests are highly inneficient because fixtures are not implemented yet.
