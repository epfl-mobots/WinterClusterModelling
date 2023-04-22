from processing_py import *
import time
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
import keyboard
import datetime

from hive import Hive
import draw


class Sim:
    def __init__(self,sim_time,hive_param,draw_on=True):
        #create save directory for plots and data
        path = '../data/'
        today = datetime.datetime.now()
        todaystr = today.isoformat()
        todaystr = todaystr.replace(":","_")[0:19]
        self.savepath = path+todaystr+'/'
        if not os.path.isdir(path+todaystr):
            os.mkdir(path+todaystr)

        f = open(self.savepath+"parameters.txt", "a")
        for k, v in hive_param.items():
            f.write(str(k) + ' : '+ str(v) + '\n\n')
        f.close()

        self.count=0

        #initialize hive and graphic
        self.hive = Hive(hive_param,sim_time)
        self.draw_on = draw_on
        if draw_on:
            self.app = App(sim_param["dims_draw"][0],sim_param["dims_draw"][1])
            self.start_graphic()
        
        
        
    def start_graphic(self):
        draw.init_world(self.app)
        draw.init_temp(self.app,self.hive)
        draw.init_colony(self.app,self.hive)

    def update(self):
        self.hive.update(self.count)
        self.count+=1
        if self.draw_on and self.count%DRAW_T==0:
            draw.update(self.app,self.hive)
    
    def end(self):
        f = open(self.savepath+"beeGrid.obj", "wb")
        pickle.dump(self.hive.beeGrid,f)
        f.close()

        f = open(self.savepath+"T_field.obj", "wb")
        pickle.dump(self.hive.tempField_save,f)
        f.close()

        f = open(self.savepath+"Tc.obj", "wb")
        pickle.dump(self.hive.Tc,f)
        f.close()

        f = open(self.savepath+"Tmax.obj", "wb")
        pickle.dump(self.hive.Tmax,f)
        f.close()

        f = open(self.savepath+"meanT.obj", "wb")
        pickle.dump(self.hive.meanT,f)
        f.close()

        f = open(self.savepath+"sigT.obj", "wb")
        pickle.dump(self.hive.sigT,f)
        f.close()
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
    "ymax"  : 99
}

hotspot_param = {
    "coord" : [[0,3],[1,3]],
    "Tspot" : 25,
}

# temp_param = {
#     "dims_temp" : (100,100), #twice as big as dims_b in Sumpter (twice finer grid)
#     "tempA" : 18,
#     "lambda_air" : 1.0,
#     "lambda_bee" : 0.45
# }

hive_param = {
    "init_shape" : "disc",
    "dims_b" : (bee_param["xmax"]+1,bee_param["ymax"]+1),
    "n_bees" : 200,
    "tau" : 8,
    "g" : 2,
    "bee_param" : bee_param,
    "dims_temp" : (100,200), #twice as big as dims_b in Sumpter (twice finer grid)
    "tempA" : 13,
    "lambda_air" : 1.0,
    "lambda_bee" : 0.45,
    "hq20" : 0.037,#0.0037,
    "gamma" : np.log(2.4)/10
}

SIM_TIME = 2 #in bee timesteps
DRAW_T = 100 #the simulation is redrawn every DRAW_T steps

sim = Sim(SIM_TIME,hive_param,draw_on=True)
for i in range(SIM_TIME):  
    sim.update()
    print(i)

#keyboard.wait('q')
plt.plot(range(SIM_TIME-1),sim.hive.Tc[1:])
plt.show()
sim.end()