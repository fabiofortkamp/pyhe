# Comparison between steady-state Carnot and simple Rankine cycles

Consider a simple Rankine cycle (no superheat) between given condenser and boiler pressures, below the critical pressure of water. 

Fit a Carnot cycle between these boundaries, such that the isothermal heat transfer in the hot side occur in the boiler pressure, between states of saturated liquid and saturated steam.

The script `run_experiments.py` analyzes this problem and generates a plot of specific work and thermal efficiency of the two cycles, varying the boiler pressure; the figure is saved in `comparison_carnot_simple_rankine.png`. It also plots the turbine and pump work components for the Simple Rankine cycle and saves the plot in `component_power_simple_rankine.png`.
