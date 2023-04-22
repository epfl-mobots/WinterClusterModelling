from sim import Sim
import numpy as np

#default parameters
bee_param = {
    "Tcoma" : 8,
    "TminI" : 18,
    "TmaxI" : 23,
    "xmax"  : 49,
    "ymax"  : 99
}

hotspot = {
    "coord" : [[0,3],[1,3]], #change
    "Tspot" : 20.5, #change
    "on" : 15 #change
}

hive_param = {
    "init_shape" : "random",
    "dims_b" : (50,100),
    "n_bees" : 200,
    "tau" : 8,
    "g" : 2,
    "bee_param" : bee_param,
    "dims_temp" : (100,200), 
    "tempA" : 13,  #change
    "lambda_air" : 1.0,
    "lambda_bee" : 0.45,
    "hq20" : 0.037,
    "gamma" : np.log(2.4)/10
}

SIM_TIME = 200 #in bee timesteps
DRAW_T = 10 #the simulation is redrawn every DRAW_T steps

sim = Sim(hive_param,draw_on=True,hotspot=hotspot,draw_t=DRAW_T)
for i in range(SIM_TIME):
    sim.update()
    print(i)

sim.end()