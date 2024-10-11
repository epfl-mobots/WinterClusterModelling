"""Definition of Frame class which handles the agents (Bee objects) and the temperature field."""

import numpy as np
import random
from configparser import ConfigParser
import ast

from bee import Bee, FREE, STAT, MOV, initBeeBehaviour


class Frame:
    def __init__(self, cfg_path):
        """Initialisation of Frame object
        cfg_path : canonical path to the config file
        graphpath : path to somewhere to store data for this exp
        """
        cfg = ConfigParser()
        cfg.read(cfg_path)

        #Store basic parameters:
        self.tau = cfg.getint('hive','tau')
        self.g = cfg.getint('hive','g')
        self.dims_b = ast.literal_eval(cfg.get('hive','dims_b'))
        self.l_bee = cfg.getfloat('hive','lambda_bee')
        self.l_air = cfg.getfloat('hive','lambda_air')
        self.hq20 = cfg.getfloat('hive','hq20')
        self.gamma = cfg.getfloat('hive','gamma')
        self.t_amb = cfg.getfloat('hive','t_amb')

        #temperature field initialisation - initially homogenous at ambient temperature
        self.dims_temp = tuple(self.g*dim for dim in self.dims_b)
        self.tempField = self.t_amb*np.ones(self.dims_temp)

        # Hotspot initialisation
        if cfg.getboolean('hotspot','used'):
            self.hot_used=True
            self.hot_on=False
            self.hotspot_on=cfg.getint('hotspot','on')
            self.hotspot_off=cfg.getint('hotspot','off')
            if cfg.get('hotspot','coord') != '':
                #computing positions of all physical hotspots depending on the temperature field dimensions
                self.i_hot = [int(0.1*self.dims_temp[0]),int(0.56*self.dims_temp[0])]
                self.j_hot = [int((0.03+0.4*k)*self.dims_temp[0]) for k in range(5)]
                self.sz_spot = int(0.34*self.dims_temp[0])

                #setting position of hotspot
                coords=ast.literal_eval(cfg.get('hotspot','coord'))
                self.n_spot = len(coords)
                self.hotspot_i = [[self.i_hot[i],self.i_hot[i]+self.sz_spot] for [i,_] in coords]
                self.hotspot_j = [[self.j_hot[j],self.j_hot[j]+self.sz_spot] for [_,j] in coords]
            else:
                self.n_spot = 1
                self.hotspot_i = [[int(cfg.getfloat('hotspot','i_c')*self.dims_temp[0]-cfg.getfloat('hotspot','sz')*self.dims_temp[0]/2),int((cfg.getfloat('hotspot','i_c')*self.dims_temp[0]+cfg.getfloat('hotspot','sz')*self.dims_temp[0]/2))]]
                self.hotspot_j = [[int((cfg.getfloat('hotspot','j_c')*self.dims_temp[1]-cfg.getfloat('hotspot','sz')*self.dims_temp[0]/2)),int((cfg.getfloat('hotspot','j_c')*self.dims_temp[1]+cfg.getfloat('hotspot','sz')*self.dims_temp[0]/2))]]
               
                self.Tspot = cfg.getfloat('hotspot','Tspot')
                if self.hotspot_on==0:
                    self.set_hotspot()
        else:
            self.hot_used=False
            self.hot_on=False

        #history of temperature field at every timestep
        self.tempField_save = [self.tempField]

        self.beeTempField = self.t_amb*np.ones(self.dims_b) # T° field for bees
        self.Tmax = [self.t_amb]                            # History of max T°
        self.Tcs = [self.t_amb]                             # History of T° at centroid
        self.Tmax_j = [0]                                   # History of j coordinate of max T° position
        self.meanT = [self.t_amb]                           # History of mean T°
        self.sigT = [0]                                     # History of std T°

        #colony initialisation
        self.n_bees = cfg.getint('hive','n_bees')
        self.beeGrid = np.zeros(self.dims_b)                # Grid of bees
        self.colony = np.asarray(self.init_colony(self.n_bees,cfg.get('hive','init_shape'),cfg['bee'])) #List of bees
        self.centroid = np.mean(np.argwhere(self.beeGrid),axis=0)
        self.bgs_save = [self.beeGrid.copy()]

        #2nd layer of beeGrid for bees in 'leave' state
        self.beeGrid_2nd = np.zeros(self.dims_b)
        self.bgs2_save = [self.beeGrid_2nd.copy()]

        #initial stage where only the temperature dynamics are active (no agent movement)
        #self.init_temp()


    def init_colony(self,_n_bees,_init_shape,_bee_param):
        """Build the list of agents (Bee objects) by random draw according to param."""
        initBeeBehaviour(_bee_param) # Initialise bee behaviour based on _bee_param
        
        bs = []
        for _ in range(_n_bees):
            if _init_shape=="disc": #initially in disc offset from corner
                offset = (self.dims_b[0]//2,self.dims_b[1]//4)
                r = int(np.sqrt(2*_n_bees//np.pi))*random.random()
                theta = 2*np.pi*random.random()
                i_b = int(r*np.cos(theta))+offset[0]
                j_b = int(r*np.sin(theta))+offset[1]
                while self.beeGrid[i_b,j_b]!=FREE:
                    r = int(np.sqrt(2*_n_bees//np.pi))*random.random()
                    theta = 2*np.pi*random.random()
                    i_b = int(r*np.cos(theta))+offset[0]
                    j_b = int(r*np.sin(theta))+offset[1]

            elif _init_shape=="ring": #initially in ring in middle
                r = 7*random.random()
                theta = 2*np.pi*random.random()
                i_b = int((r+2)*np.cos(theta))+self.dims_b[0]//2
                j_b = int((r+2)*np.sin(theta))+self.dims_b[1]//2
                while self.beeGrid[i_b,j_b]!=FREE:
                    r = 10*random.random()
                    theta = 2*np.pi*random.random()
                    i_b = int((r+2)*np.cos(theta))+self.dims_b[0]//2
                    j_b = int((r+2)*np.sin(theta))+self.dims_b[1]//2

            else: #random initialisation across grid
                i_b =int(random.random()*(self.dims_b[0]))
                j_b =int(random.random()*(self.dims_b[1])/2) # Spawn bees only on left side
                while self.beeGrid[i_b,j_b]!=FREE:
                    i_b = int(random.random()*(self.dims_b[0]))
                    j_b = int(random.random()*(self.dims_b[1])/2)
            
            self.beeGrid[i_b,j_b] = STAT        
            bs.append(Bee(i_b,j_b,_bee_param))
        return bs
    
    def reset_params(self, cfg_path):
        '''Resets the parameters of the frame to the ones provided in the cfg file
        - cfg_path : canonical path to the new config file '''
        cfg = ConfigParser()
        cfg.read(cfg_path)

        #Store basic parameters:
        self.tau = cfg.getint('hive','tau')
        self.g = cfg.getint('hive','g')
        self.dims_b = ast.literal_eval(cfg.get('hive','dims_b'))
        self.l_bee = cfg.getfloat('hive','lambda_bee')
        self.l_air = cfg.getfloat('hive','lambda_air')
        self.hq20 = cfg.getfloat('hive','hq20')
        self.gamma = cfg.getfloat('hive','gamma')
        self.t_amb = cfg.getfloat('hive','t_amb')

        if cfg.getboolean('hotspot','used'):
            self.hot_used=True
            self.hot_on=False
            self.hotspot_on=cfg.getint('hotspot','on')
            self.hotspot_off=cfg.getint('hotspot','off')
            if cfg.get('hotspot','coord') != '':
                #computing positions of all physical hotspots depending on the temperature field dimensions
                self.i_hot = [int(0.1*self.dims_temp[0]),int(0.56*self.dims_temp[0])]
                self.j_hot = [int((0.03+0.4*k)*self.dims_temp[0]) for k in range(5)]
                self.sz_spot = int(0.34*self.dims_temp[0])

                #setting position of hotspot
                coords=ast.literal_eval(cfg.get('hotspot','coord'))
                self.n_spot = len(coords)
                self.hotspot_i = [[self.i_hot[i],self.i_hot[i]+self.sz_spot] for [i,_] in coords]
                self.hotspot_j = [[self.j_hot[j],self.j_hot[j]+self.sz_spot] for [_,j] in coords]
            else:
                self.n_spot = 1
                self.hotspot_i = [[int(cfg.getfloat('hotspot','i_c')*self.dims_temp[0]-cfg.getfloat('hotspot','sz')*self.dims_temp[0]/2),int((cfg.getfloat('hotspot','i_c')*self.dims_temp[0]+cfg.getfloat('hotspot','sz')*self.dims_temp[0]/2))]]
                self.hotspot_j = [[int((cfg.getfloat('hotspot','j_c')*self.dims_temp[1]-cfg.getfloat('hotspot','sz')*self.dims_temp[0]/2)),int((cfg.getfloat('hotspot','j_c')*self.dims_temp[1]+cfg.getfloat('hotspot','sz')*self.dims_temp[0]/2))]]
               
                self.Tspot = cfg.getfloat('hotspot','Tspot')
                if self.hotspot_on==0:
                    self.set_hotspot()
        else:
            self.hot_used=False
            self.hot_on=False

    def init_temp(self):
        """Update the temperature field only (no agent movement)"""
        for _ in range(1000):
            self.update_temp()

    def set_hotspot(self):
        """Turn on the hotspot. Sets its area to a fixed temperature."""
        self.hot_on = True
        for a,b in zip(self.hotspot_i,self.hotspot_j):
            self.tempField[a[0]:a[1],b[0]:b[1]] = self.Tspot

    def f(self,i,j):
        """Compute the metabolic temperature contribution of the agent at position (i,j).
        Returns 0 if no agent is at this position.
        """
        f_ij = self.hq20*np.exp(self.gamma*(self.beeTempField[i//self.g,j//self.g]-20)) if (self.beeGrid[i//self.g,j//self.g]!=FREE) else 0
        return f_ij

    def diff(self,i,j,lamdas):
        """Compute the diffusion term in the temperature equation for position (i,j).
            Lij=La-Pij*(La-Lb) --> We first compute Pij
        """
        d = 0
        #l=self.l_air-Pij[i//2,j//2]*(self.l_air-self.l_bee)
        #lamdas = self.l_bee if (self.beeGrid==STAT) else self.l_air

        for ip,jp in zip([i-1,i,i+1,i],[j,j-1,j,j+1]):
            #lp = self.l_bee if self.beeGrid[ip//2,jp//2]==STAT else self.l_air
            d += lamdas[i//self.g,j//self.g]*lamdas[ip//self.g,jp//self.g]*(self.tempField[ip,jp]-self.tempField[i,j])

        return d/4  

    def h(self,i,j):
        """Checks whether position (i,j) is within the boundaries of the hotspot."""
        for n in range(self.n_spot):
            if i>self.hotspot_i[n][0] and i<self.hotspot_i[n][1] and j>self.hotspot_j[n][0] and j<self.hotspot_j[n][1]:
                return n
        return -1

    def update_temp(self,lamdas):
        """Update the temperature field."""
        tempField_ = self.tempField
        for i in range(1,self.dims_temp[0]-1): # Exclude borders because initial condition
            for j in range(1,self.dims_temp[1]-1):
                if self.hot_on:
                    hotspot= self.h(i,j)
                    if hotspot!=-1:
                        j=self.hotspot_j[hotspot][1]-1 #Skips all other pixels on the hotspot
                        continue
                diffusion_term= self.diff(i,j,lamdas)
                heating = self.f(i,j)
                tempField_[i,j] += diffusion_term + heating
        self.tempField = tempField_
        
    def update(self,count):
        """Update the Frame state. Called at each timestep.
        - count is the iteration number
        """
        if self.hot_used: # Hotspot management
            if self.hotspot_on==count:
                self.set_hotspot()
            elif self.hot_on and self.hotspot_off==count:
                self.hot_on = False

        # tau temperature updates for each bee update
        Pij=(self.beeGrid)%2
        lamdas=self.l_air-Pij*(self.l_air-self.l_bee)
        for _ in range(self.tau):
            self.update_temp(lamdas)
        
        # update measurements of temp history
        self.Tmax.append(np.amax(self.tempField))
        self.Tmax_j.append(np.unravel_index(np.argmax(self.tempField, axis=None), self.tempField.shape)[1]) # j position of max T°
        self.meanT.append(np.mean(self.tempField))
        self.sigT.append(np.std(self.tempField))
        
        #Compute the temperature felt by the agents and update them
        self.compute_Tbee()
        idxs = np.arange(self.colony.size)
        np.random.shuffle(idxs)
        for i in idxs:
            self.colony[i].update(self.beeTempField,self.beeGrid,self.beeGrid_2nd)
        
        #Saving state
        self.centroid = np.mean(np.argwhere(self.beeGrid),axis=0)
        self.Tcs.append(self.beeTempField[int(self.centroid[0]),int(self.centroid[1])])
        self.tempField_save.append(self.tempField.copy())
        self.bgs_save.append(self.beeGrid.copy())
        self.bgs2_save.append(self.beeGrid_2nd.copy())
        
    
    def compute_Tbee(self):
        """Compute local average of temperature at each possible agent position."""
        #   From https://stackoverflow.com/questions/26871083/how-can-i-vectorize-the-averaging-of-2x2-sub-arrays-of-numpy-array :
        #   Using the reshape method for faster computation
        beeTempField = self.tempField.reshape(np.shape(self.tempField)[0]//2, 2, np.shape(self.tempField)[1]//2, 2)
        self.beeTempField = beeTempField.mean(axis=(1,3))