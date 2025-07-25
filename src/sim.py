"""Definition of Sim class handling the saving and calling graphics generation"""
import os, datetime
import pickle
from configparser import ConfigParser
import shutil
import draw
import ast

from frame import Frame


class Sim:
    def __init__(self,cfg_path=None, frame_save=None):
        """Initialisation of the simulation
        cfg_path : path the the cfg file of the Simulation
        frame_saved : None or path of Frame object to load from
        """
        # Find the right config file, either provided or from save
        cfg = ConfigParser()
        if cfg_path is not None:
            # new config provided (either for new frame or for saved frame)
            cfg.read(cfg_path)
        else:
            # Find cfg file in frame save
            cfg.read(frame_save+"/config_copy")

        #Create save directory for data
        self.dict_Tamb = {key: ast.literal_eval(value) for key, value in cfg['Tamb_dictionnary'].items()}
        if len(self.dict_Tamb) == 1 :
            t_amb=self.dict_Tamb['t0']['Temperature']
        else:
            t_amb = 'Multiple Temperatures'
        if cfg.get('bee','BH') == 'sumpter':
            if t_amb == 'Multiple Temperatures':
                path = f'../data/{t_amb}/sumpter/'
            else:
                path = f'../data/{t_amb}C/sumpter/'
        elif cfg.get('bee','BH') == 'explorer':
            if t_amb == 'Multiple Temperatures':
                path = f'../data/{t_amb}/explore/'
            else :
                path = f'../data/{t_amb}C/explore/'
        else:
            raise ValueError(f"Invalid bee mode: {cfg.get('bee','BH')}")

        todaystr = datetime.datetime.now().isoformat()
        todaystr = todaystr.replace(":","_")[0:19]
        self.savepath = path+todaystr+'/'

        if not os.path.isdir(path+todaystr):
            os.makedirs(path+todaystr)
            os.makedirs(path+todaystr+"/graphics")

        # Save parameters as a cfg file in the data directory
        shutil.copyfile(cfg_path, self.savepath+"config_copy")

        # Initialise Frame
        if frame_save is not None and cfg_path is None:
            # Use saved Frame with its own cfg file
            f = open(frame_save+"/frame.obj", "rb")
            self.frame = pickle.load(f)
            f.close()
        elif frame_save is not None and cfg_path is not None:
            # Use saved Frame with new cfg file
            # Load frame from checkpoint:
            f = open(frame_save+"/frame.obj", "rb")
            self.frame = pickle.load(f)
            f.close()
            self.frame.reset_params(cfg_path) #Overrides current params with the new cfg file 
        else:
            # Start new frame from scratch
            self.frame = Frame(cfg_path)

        # Handle graphics:
        self.draw_on=cfg.getboolean('simu','draw_on', fallback=False)
        if self.draw_on:
            self.savegraphpath = self.savepath+"graphics/"
            self.start_graphic()
            self.draw_t = cfg.getint('simu','refresh_rate')
            
        # Meta simu variables:
        self.count=0
        self.simu_steps=cfg.getint('simu','simu_steps')
        self.save_freq=cfg.getint('simu','save_freq')
        
        
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
        path = self.savepath+f"/it_{self.count}"
        if not os.path.isdir(path):
            os.mkdir(path)
        file = open(path+"/frame.obj", "wb")
        pickle.dump(self.frame,file)
        file.close()

    """
    Not used
    """
    def save_old(self):
        pat = self.savepath+'/it_{}'.format(self.count)
        if not os.path.isdir(pat):
            os.mkdir(pat)
        pat = pat+'/'
        f = open(pat+"beeGrid.obj", "wb")
        pickle.dump(self.frame.bg_history,f)
        f.close()

        f = open(pat+"beeGrid_2nd.obj", "wb")
        pickle.dump(self.frame.bg2_history,f)
        f.close()

        f = open(pat+"T_field.obj", "wb")
        pickle.dump(self.frame.tempField_history,f)
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
