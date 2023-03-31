from processing_py import *
import time
import numpy as np
import matplotlib.pyplot as plt
import keyboard

from hive import Hive
import draw


class Sim:
    def __init__(self,sim_param,hive_param,draw_on=True):
        self.hive = Hive(hive_param)
        self.draw_on = draw_on
        if draw_on:
            #self.app = App(sim_param["dims_draw"][0],sim_param["dims_draw"][1])
            self.start_graphic()
        self.count=0
    
    def start_graphic(self):
        draw.update(self.hive)

    def update(self):
        self.hive.update()
        self.count+=1
        if self.draw_on and self.count%DRAW_T==0:
            draw.update(self.hive,self.count)
    
    def end(self):
        return

#------------------------------------------------------------------------------
sim_param = {
    "dims_draw" : (800,800)
}

bee_param = {
    "Tcoma" : 8,
    "TminI" : 18,
    "TmaxI" : 23,
    "xmax"  : 49,
    "ymax"  : 49
}

# temp_param = {
#     "dims_temp" : (100,100), #twice as big as dims_b in Sumpter (twice finer grid)
#     "tempA" : 18,
#     "lambda_air" : 1.0,
#     "lambda_bee" : 0.45
# }

hive_param = {
    "init_shape" : "random",
    "dims_b" : (50,50),
    "n_bees" : 200,
    "tau" : 8,
    "g" : 2,
    "bee_param" : bee_param,
    "dims_temp" : (100,100), #twice as big as dims_b in Sumpter (twice finer grid)
    "tempA" : 13,
    "lambda_air" : 1.0,
    "lambda_bee" : 0.45,
    "hq20" : 0.037,#0.0037,
    "gamma" : np.log(2.4)/10
}

SIM_TIME = 10000 #in bee timesteps
DRAW_T = 5000 #the simulation is redrawn every DRAW_T steps

sim = Sim(sim_param,hive_param,draw_on=True)
for i in range(SIM_TIME):
    sim.update()
    print(i)

keyboard.wait('q')
plt.plot(range(SIM_TIME+1),sim.hive.Tmax)
plt.show()
sim.end()