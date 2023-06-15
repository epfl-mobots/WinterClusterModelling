"""Definition of Sim class handling the saving and calling graphics generation"""
import os, datetime
import numpy as np
import matplotlib.pyplot as plt
import pickle

from hive import Hive
import draw


class Sim:
    def __init__(self,hive_param,draw_on=True,hotspot=False,draw_t=10, load_saved=False):
        """Initialisation of the simulation
        hive_param : parameters of the hive
        draw_on : boolean value for graphics generation (no graphics if False)
        hotspot : False or hotspot parameters
        draw_t : graphics refresh rate (in number of simulation timesteps)
        load_saved : False or path of Hive object to load from
        """
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

        if type(load_saved)==bool:
            #initialize hive and graphic
            self.hive = Hive(hive_param,hotspot)
        else:
            f = open(load_saved+"/hive.obj", "rb")
            self.hive = pickle.load(f)
            f.close()
        
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
        f = open(pat+"hive.obj", "wb")
        pickle.dump(self.hive,f)
        f.close()

    def save_old(self):
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
