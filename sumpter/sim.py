import os, datetime
import numpy as np
import matplotlib.pyplot as plt
import pickle

from hive import Hive
import draw


class Sim:
    def __init__(self,hive_param,draw_on=True,hotspot=False,draw_t=10):
        #create save directory for plots and data
        if hive_param["bee_param"]["alpha"]==0:
            path = '../data/{}C/sump/'.format(hive_param["tempA"])
        else:
            path = '../data/{}C/exp/'.format(hive_param["tempA"])

        today = datetime.datetime.now()
        todaystr = today.isoformat()
        todaystr = todaystr.replace(":","_")[0:19]
        self.savepath = path+todaystr+'/'
        self.savegraphpath = path+todaystr+"/graphics/"
        if not os.path.isdir(path+todaystr):
            os.mkdir(path+todaystr)
            os.mkdir(path+todaystr+"/graphics")

        f = open(self.savepath+"parameters.txt", "a")
        for k, v in hive_param.items():
            f.write(str(k) + ' : '+ str(v) + '\n\n')
            
        for k, v in hotspot.items():
            f.write(str(k) + ' : '+ str(v) + '\n\n')
        f.close()

        #initialize hive and graphic
        self.hive = Hive(hive_param,hotspot)
        self.draw_on = draw_on
        if draw_on:
            self.start_graphic()
        
        self.draw_t = draw_t
        self.count=0
        
        
    def start_graphic(self):
        draw.update(self.hive,self.savegraphpath)

    def update(self):
        self.hive.update(self.count)
        self.count+=1
        if self.draw_on and self.count%self.draw_t==0:
            draw.update(self.hive,self.savegraphpath,self.count)
    
    def end(self):
        self.save()
        return
    
    def save(self):
        pat = self.savepath+'/it_{}'.format(self.count)
        if not os.path.isdir(pat):
            os.mkdir(pat)
        pat = pat+'/'
        f = open(pat+"beeGrid.obj", "wb")
        pickle.dump(self.hive.bg_save,f)
        f.close()

        f = open(pat+"beeGrid_2nd.obj", "wb")
        pickle.dump(self.hive.bg2_save,f)
        f.close()

        f = open(pat+"T_field.obj", "wb")
        pickle.dump(self.hive.tempField_save,f)
        f.close()

        f = open(pat+"Tc.obj", "wb")
        pickle.dump(self.hive.Tc,f)
        f.close()

        f = open(pat+"Tmax.obj", "wb")
        pickle.dump(self.hive.Tmax,f)
        f.close()

        f = open(pat+"meanT.obj", "wb")
        pickle.dump(self.hive.meanT,f)
        f.close()

        f = open(pat+"sigT.obj", "wb")
        pickle.dump(self.hive.sigT,f)
        f.close()
        return

# #------------------------------------------------------------------------------

# bee_param = {
#     "Tcoma" : 8,
#     "TminI" : 18,
#     "TmaxI" : 23,
#     "xmax"  : 49,
#     "ymax"  : 99
# }

# hotspot = {
#     "coord" : [[0,3],[1,3]],
#     "Tspot" : 25,
#     "on" : 0
# }

# hive_param = {
#     "init_shape" : "disc",
#     "dims_b" : (50,100),
#     "n_bees" : 200,
#     "tau" : 13,
#     "g" : 2,
#     "bee_param" : bee_param,
#     "dims_temp" : (100,200), #twice as big as dims_b in Sumpter (twice finer grid)
#     "tempA" : 13,
#     "lambda_air" : 1.0,
#     "lambda_bee" : 0.45,
#     "hq20" : 0.037,#0.0037,
#     "gamma" : np.log(2.4)/10
# }

# SIM_TIME = 200 #in bee timesteps
# DRAW_T = 10 #the simulation is redrawn every DRAW_T steps

# sim = Sim(hive_param,draw_on=True,hotspot=hotspot)
# for i in range(SIM_TIME):
#     sim.update()
#     print(i)

# #keyboard.wait('q')
# plt.plot(range(SIM_TIME),sim.hive.Tc[1:])
# plt.show()
# sim.end()