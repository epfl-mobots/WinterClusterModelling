import os, datetime
import numpy as np
import matplotlib.pyplot as plt
import pickle

from hive import Hive
import draw


class Sim:
    def __init__(self,hive_param,draw_on=True):
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

        #initialize hive and graphic
        self.hive = Hive(hive_param)
        self.draw_on = draw_on
        if draw_on:
            self.start_graphic()
        self.count=0
        
        
    def start_graphic(self):
        draw.update(self.hive,self.savepath)

    def update(self):
        self.hive.update()
        self.count+=1
        if self.draw_on and self.count%DRAW_T==0:
            draw.update(self.hive,self.savepath,self.count)
    
    def end(self):
        f = open(self.savepath+"beeGrid.obj", "wb")
        pickle.dump(self.hive.beeGrid,f)
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

bee_param = {
    "Tcoma" : 8,
    "TminI" : 18,
    "TmaxI" : 23,
    "xmax"  : 49,
    "ymax"  : 49
}

hive_param = {
    "init_shape" : "random",
    "dims_b" : (50,50),
    "n_bees" : 200,
    "tau" : 13,
    "g" : 2,
    "bee_param" : bee_param,
    "dims_temp" : (100,100), #twice as big as dims_b in Sumpter (twice finer grid)
    "tempA" : 13,
    "lambda_air" : 1.0,
    "lambda_bee" : 0.45,
    "hq20" : 0.037,#0.0037,
    "gamma" : np.log(2.4)/10
}

SIM_TIME = 2000 #in bee timesteps
DRAW_T = 1000 #the simulation is redrawn every DRAW_T steps

sim = Sim(hive_param,draw_on=True)
for i in range(SIM_TIME):
    sim.update()
    print(i)

#keyboard.wait('q')
plt.plot(range(SIM_TIME),sim.hive.Tc[1:])
plt.show()
sim.end()