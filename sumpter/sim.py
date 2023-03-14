from processing_py import *
import time

from hive import Hive
from temp_field import TempField
from sim_parameters import SimParam
import draw


SIM_TIME=1000 #in bee timesteps

class Sim:
    def __init__(self,sim_param,hive_param,draw_on=True):
        self.hive = Hive(hive_param)
        self.draw_on = draw_on
        if draw_on:
            self.app = App(sim_param["dims_draw"][0],sim_param["dims_draw"][1])        
            self.start_graphic()
    
    def start_graphic(self):
        draw.init_world(self.app)
        draw.init_temp(self.app,self.hive)
        draw.init_colony(self.app,self.hive)

    def update(self):
        self.hive.update()
        if self.draw_on:
            draw.update(self.hive)
    
    def end(self):
        if self.draw_on:
            self.app.exit()

#------------------------------------------------------------------------------
sim_param = {
    "dims_draw" : (800,800)
}

bee_param = {
    "Tcoma" : 8,
    "TminI" : 18,
    "TmaxI" : 23
}

temp_param = {
    "dims_temp" : (100,100), #twice as big as dims_b in Sumpter (twice finer grid)
    "tempA" : 12,
    "lambda_air" : 1.0,
    "lambda_bee" : 0.45
}

hive_param = {
    "dims_b" : (50,50),
    "n_bees" : 100,
    "tau" : 8,
    "g" : 2,
    "bee_param" : bee_param,
    "temp_param" : temp_param
}

sim = Sim(sim_param,hive_param,draw_on=True)
for i in range(SIM_TIME):
    sim.update()
time.sleep(10)
sim.end()
