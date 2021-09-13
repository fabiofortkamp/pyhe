import numpy as np
from CoolProp.CoolProp import PropsSI
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

from pyhe import CarnotSteadyStateCycle, SimpleRankineCycle

plt.rcParams.update({'font.size': 14})

TEMPERATURE_BOILER = 85 + 273.15
TEMPERATURE_CONDENSER = 40 + 273.15
N_POINTS = 11

FIGSIZE_WIDTH_CM = 24
FIGSIZE_HEIGHT_CM = FIGSIZE_WIDTH_CM*9/16

FIGSIZE_WIDTH = FIGSIZE_WIDTH_CM/2.54
FIGSIZE_HEIGHT = FIGSIZE_HEIGHT_CM/2.54

fluids = ['R134a','Water','Ammonia']
n_fluids = len(fluids)

P_boiler = np.empty(n_fluids)
P_condenser = np.empty(n_fluids)
w = np.empty(n_fluids)
eta = np.empty(n_fluids)

for (i,fluid) in enumerate(fluids):

    P_boiler[i] = PropsSI("P","T",TEMPERATURE_BOILER,"Q",1,fluid)
    P_condenser[i] = PropsSI("P","T",TEMPERATURE_CONDENSER,"Q",1,fluid)

    src = SimpleRankineCycle(P_condenser[i],P_boiler[i],fluid=fluid)
    src.run()
    eta[i] = src.metrics["Thermal efficiency"]
    w[i] = src.metrics["Specific work"]

fig_eta, ax_eta = plt.subplots(figsize=(FIGSIZE_WIDTH,FIGSIZE_HEIGHT))
y_pos = np.arange(len(fluids))
ax_eta.barh(y_pos,100*eta)
ax_eta.set_yticks(y_pos)
ax_eta.set_yticklabels(fluids)
ax_eta.set_xlabel("Thermal Efficiency [%]")
ax_eta.set_title(
    "Performance of Simple Rankine cycle with condenser temperature of %.2f K and boiler temperature of %.2f K" %(TEMPERATURE_CONDENSER,TEMPERATURE_BOILER),wrap=True,loc='left'
)

fig_eta.savefig("efficiency_fluids_simple_rankine.png",dpi=600)


fig_w, ax_w = plt.subplots(figsize=(FIGSIZE_WIDTH,FIGSIZE_HEIGHT))

ax_w.barh(y_pos,1e-3*w)
ax_w.set_yticks(y_pos)
ax_w.set_yticklabels(fluids)
ax_w.set_xlabel("Specific work [kJ/kg]")
ax_w.set_title(
    "Performance of Simple Rankine cycle with condenser temperature of %.2f K and boiler temperature of %.2f K" %(TEMPERATURE_CONDENSER,TEMPERATURE_BOILER),wrap=True,loc='left'
)
fig_w.savefig("w_fluids_simple_rankine.png",dpi=600)


fig_Pb, ax_Pb = plt.subplots(figsize=(FIGSIZE_WIDTH,FIGSIZE_HEIGHT))
ax_Pb.barh(y_pos,1e-3*P_boiler)
ax_Pb.set_yticks(y_pos)
ax_Pb.set_yticklabels(fluids)
ax_Pb.set_xlabel("Boiler pressure [kPa]")
ax_Pb.set_title(
    "Performance of Simple Rankine cycle with condenser temperature of %.2f K and boiler temperature of %.2f K" %(TEMPERATURE_CONDENSER,TEMPERATURE_BOILER),wrap=True,loc='left'
)
fig_Pb.savefig("Pboiler_fluids_simple_rankine.png",dpi=600)

fig_Pc, ax_Pc = plt.subplots(figsize=(FIGSIZE_WIDTH,FIGSIZE_HEIGHT))
ax_Pc.barh(y_pos,1e-3*P_condenser)
ax_Pc.set_yticks(y_pos)
ax_Pc.set_yticklabels(fluids)
ax_Pc.set_xlabel("Condenser pressure [kPa]")
ax_Pc.set_title(
    "Performance of Simple Rankine cycle with condenser temperature of %.2f K and boiler temperature of %.2f K" %(TEMPERATURE_CONDENSER,TEMPERATURE_BOILER),wrap=True,loc='left'
)
fig_Pc.savefig("Pcondender_fluids_simple_rankine.png",dpi=600)