"""Definition of Sim class handling the saving and calling graphics generation"""
import os, datetime
import pickle
from configparser import ConfigParser
import shutil

from frame import Frame
import draw


class Sim:
    def __init__(self,cfg_path=None,draw_on=True,draw_t=10, load_saved=False):
        """Initialisation of the simulation
        frame_param : parameters of the frame
        draw_on : boolean value for graphics generation (no graphics if False)
        hotspot : False or hotspot parameters
        draw_t : graphics refresh rate (in number of simulation timesteps)
        load_saved : False or path of Frame object to load from
        """
        if load_saved is False:
            cfg = ConfigParser()
            cfg.read(cfg_path)

            #Create save directory for plots and data
            t_amb=cfg.getfloat('hive','t_amb')
            if cfg.get('bee','alpha') == '' or cfg.getfloat('bee','alpha')== 0.0:
                path = f'../data/{t_amb}C/sump/'
            else:
                path = f'../data/{t_amb}C/exp/'

            todaystr = datetime.datetime.now().isoformat()
            todaystr = todaystr.replace(":","_")[0:19]
            self.savepath = path+todaystr+'/'
            self.savegraphpath = self.savepath+"graphics/"

            if not os.path.isdir(path+todaystr):
                os.makedirs(path+todaystr)
                os.makedirs(path+todaystr+"/graphics")

            # Save parameters as a cfg file in the dir
            shutil.copyfile(cfg_path, self.savepath+"config_copy")

            self.frame = Frame(cfg_path,self.savegraphpath)

        else:
            f = open(load_saved+"/frame.obj", "rb")
            self.frame = pickle.load(f)
            f.close()
        
        self.draw_on = draw_on
        if draw_on:
            self.start_graphic()
        
        self.draw_t = draw_t
        self.count=0
        
        
    def start_graphic(self):
        draw.update(self.frame,self.savegraphpath)

    def update(self):
        self.frame.update(self.count)
        self.count+=1
        if self.draw_on and self.count%self.draw_t==0:
            draw.update(self.frame,self.savegraphpath,self.count)
    
    def end(self):
        self.save()
        return
    
    """
    Saves the Frame parameters
    """
    def save(self):
        pat = self.savepath+f"/it_{self.count}"
        if not os.path.isdir(pat):
            os.mkdir(pat)
        f = open(pat+"/frame.obj", "wb")
        pickle.dump(self.frame,f)
        f.close()

    """
    Not used
    """
    def save_old(self):
        pat = self.savepath+'/it_{}'.format(self.count)
        if not os.path.isdir(pat):
            os.mkdir(pat)
        pat = pat+'/'
        f = open(pat+"beeGrid.obj", "wb")
        pickle.dump(self.frame.bg_save,f)
        f.close()

        f = open(pat+"beeGrid_2nd.obj", "wb")
        pickle.dump(self.frame.bg2_save,f)
        f.close()

        f = open(pat+"T_field.obj", "wb")
        pickle.dump(self.frame.tempField_save,f)
        f.close()

        f = open(pat+"Tc.obj", "wb")
        pickle.dump(self.frame.Tc,f)
        f.close()

        f = open(pat+"Tmax.obj", "wb")
        pickle.dump(self.frame.Tmax,f)
        f.close()

        f = open(pat+"meanT.obj", "wb")
        pickle.dump(self.frame.meanT,f)
        f.close()

        f = open(pat+"sigT.obj", "wb")
        pickle.dump(self.frame.sigT,f)
        f.close()
        return