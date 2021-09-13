import numpy as np
from CoolProp.CoolProp import PropsSI
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

from pyhe import CarnotSteadyStateCycle, SimpleRankineCycle

PRESSURE_CONDENSER = 50e3

PRESSURE_BOILER_MIN = 0.5e6
PRESSURE_BOILER_MAX = 15e6
N_POINTS = 11

FIGSIZE_WIDTH_CM = 24
FIGSIZE_HEIGHT_CM = FIGSIZE_WIDTH_CM*9/16

FIGSIZE_WIDTH = FIGSIZE_WIDTH_CM/2.54
FIGSIZE_HEIGHT = FIGSIZE_HEIGHT_CM/2.54


FLUID = 'Water'

P_boiler = np.linspace(PRESSURE_BOILER_MIN,PRESSURE_BOILER_MAX,N_POINTS)
w_Carnot = np.empty_like(P_boiler)
w_Rankine = np.empty_like(P_boiler)
w_turbine_Rankine = np.empty_like(P_boiler)
w_pump_Rankine = np.empty_like(P_boiler)

eta_Carnot = np.empty_like(P_boiler)
eta_Rankine = np.empty_like(P_boiler)

T_L = PropsSI("T","P",PRESSURE_CONDENSER,"Q",1,FLUID)

for (i,Pb) in enumerate(P_boiler):

    T_H = PropsSI("T","P",Pb,"Q",1,FLUID)
    s_v = PropsSI("S","T",T_H,"Q",1,FLUID)
    s_l = PropsSI("S","T",T_H,"Q",0,FLUID)
    Delta_s = s_v - s_l

    cc = CarnotSteadyStateCycle(T_L,T_H,Delta_s)
    cc.run()
    eta_Carnot[i] = cc.metrics["Thermal efficiency"]
    w_Carnot[i] = cc.metrics["Specific work"]

    src = SimpleRankineCycle(PRESSURE_CONDENSER,Pb,fluid=FLUID)
    src.run()
    eta_Rankine[i] = src.metrics["Thermal efficiency"]
    w_Rankine[i] = src.metrics["Specific work"]
    w_turbine_Rankine[i] = src.metrics["Turbine work"]
    w_pump_Rankine[i] = src.metrics["Pump work"]

fig, ax = plt.subplots(figsize=(FIGSIZE_WIDTH,FIGSIZE_HEIGHT))
x = P_boiler*1e-3
ax.plot(x,100*eta_Carnot,"ko-")
ax.plot(x,100*eta_Rankine,"kx-")
ax.set_xlabel("Boiler pressure [kPa]")
ax.set_ylabel("Thermal Efficiency [%]")
ax.set_ylim((0,70))

ax.set_title("Comparison of thermal efficiency (solid lines) and specific work (dashed lines) for the Carnot (dots) and Simple Rankine (x), for a fixed condenser pressure of %.2f kPa" %(PRESSURE_CONDENSER*1e-3),loc='left',wrap=True)
ax.grid(True)
ax_w = ax.twinx()
ax_w.plot(x,1e-3*w_Carnot,"ko--")
ax_w.plot(x,1e-3*w_Rankine,"kx--")
ax_w.set_ylabel("Specific work [kJ/kg]")

# stolen from https://stackoverflow.com/questions/26752464/how-do-i-align-gridlines-for-two-y-axis-scales-using-matplotlib
ax_w.set_yticks(np.linspace(ax_w.get_yticks()[0], ax_w.get_yticks()[-1], len(ax.get_yticks())))
# from https://stackoverflow.com/questions/29188757/matplotlib-specify-format-of-floats-for-tick-labels
ax_w.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
fig.savefig("comparison_carnot_simple_rankine.png",dpi=600)

fig_power, ax_power = plt.subplots(figsize=(FIGSIZE_WIDTH,FIGSIZE_HEIGHT))
ax_power.plot(x,1e-3*w_pump_Rankine,"ko-")
ax_power.plot(x,1e-3*w_turbine_Rankine,"kx-")
ax_power.set_xlabel("Boiler pressure [kPa]")
ax_power.set_ylabel("Component work [kJ/kg]")
ax_power.set_title("Turbine (x) and pump (dot) work in a Simple Rankine cycle, for a fixed condenser pressure of %.2f kPa" %(PRESSURE_CONDENSER*1e-3),loc='left',wrap=True)
ax_power.grid(True)
fig_power.savefig("component_power_simple_rankine.png",dpi=600)
