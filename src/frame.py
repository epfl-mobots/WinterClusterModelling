"""Definition of Frame class which handles the agents (Bee objects) and the temperature field."""

import numpy as np
import random
import configparser
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
        self.l_bee = cfg.getfloat('hive','lambda_bee')
        self.l_air = cfg.getfloat('hive','lambda_air')
        self.hq20 = cfg.getfloat('hive','hq20')
        self.gamma = cfg.getfloat('hive','gamma')
        self.Kp =  cfg.getfloat('hive','Kp')
        self.dim_scaling =  cfg.getfloat('hive','3D_scaling')
        self.RealisticFrame = cfg.getboolean('hotspot','RealisticFrame')
        self.dims_b = list(ast.literal_eval(cfg.get('FreeFrame','dims_b')))
        self.outside = cfg.getfloat('RealisticFrame','outside')
        self.b = cfg.getfloat('RealisticFrame','b')
        self.t = cfg.getfloat('RealisticFrame','t')
        self.bee_surf = cfg.getfloat('RealisticFrame','bee_surf')
        self.hotspot_space = cfg.getfloat('RealisticFrame','hotspot_space')
        self.hotspot_dim = list(ast.literal_eval(cfg.get('RealisticFrame','hotspot_dim')))
        self.dict_hotspot = {key: ast.literal_eval(value) for key, value in cfg['hotspot_dictionnary'].items()}
        self.dict_Tamb = {key: ast.literal_eval(value) for key, value in cfg['Tamb_dictionnary'].items()}
        self.max_temp = cfg.getfloat('hive','max_temp')
        
        #Converting cm data in pixels
        if self.RealisticFrame:
            self.hotspot_space = self.convert_cm_to_array(self.hotspot_space)
            self.hotspot_dim[0] = self.convert_cm_to_array(self.hotspot_dim[0])
            self.hotspot_dim[1] = self.convert_cm_to_array(self.hotspot_dim[1])
            self.outside = self.convert_cm_to_array(self.outside)
            self.b = self.convert_cm_to_array(self.b)
            self.t = self.convert_cm_to_array(self.t)
        
        if self.RealisticFrame:
            #Error raising if parameters are not valid
            if len(self.dict_hotspot) % 4 != 0:
                raise configparser.ParsingError(f"Number of hotspot must be a multiple of 4")
            for location in self.dict_hotspot.keys():
                if self.dict_hotspot[location]['Temperature'] < 0 and self.dict_hotspot[location]['Temperature'] != -1:
                    raise configparser.ParsingError(f"Negative temperature not allowed, except for -1 (hotspot off)")
            if self.bee_surf <= 0:
                raise configparser.ParsingError(f"Bee surface must be positive and non-zero")
            if self.hotspot_space < 0:
                raise configparser.ParsingError(f"Hotspot space must be positive")
            if self.hotspot_dim[0] <= 0 or self.hotspot_dim[1] <= 0:
                raise configparser.ParsingError(f"Hotspot dimensions must be positive and non-zero")
            if self.outside < 0:
                raise configparser.ParsingError(f"Outside length must be positive")
            if self.b < 0:
                raise configparser.ParsingError(f"b length must be positive")
            if self.t < 0:
                raise configparser.ParsingError(f"t length must be positive")
            
            #Calculation of dimensions' frame
            self.nb_hotspots_row = len(self.dict_hotspot)/4
            self.dims_b[1] = int(self.nb_hotspots_row*self.hotspot_dim[1] + (self.nb_hotspots_row+1)*self.hotspot_space + self.outside*2)
            self.dims_b[0] = int((2*self.hotspot_dim[0] + 3*self.hotspot_space + self.outside + self.t)*2 + self.b)
            self.single_height = int(2*self.hotspot_dim[0] + 3*self.hotspot_space + self.t) 
        
        #Temperature field initialisation - initially homogenous at ambient temperature
        self.dims_temp = tuple(self.g*dim for dim in self.dims_b)
        self.Tamb = self.dict_Tamb['t0']['Temperature']
        self.tempField =self.Tamb*np.ones(self.dims_temp)
            
        # Hotspot initialisation
        if cfg.getboolean('hotspot','used'):
            self.hot_used=True
            self.hotspot_i =list()
            self.hotspot_j = list()
            self.hot_on=False
            
            #Hotspots initialisation for FreeFrame
            if self.RealisticFrame==False:
                self.hotspot_on=cfg.getint('FreeFrame','on')
                self.hotspot_off=cfg.getint('FreeFrame','off')
                self.n_spot_on = 1
                self.hotspot_i = [[int(cfg.getfloat('FreeFrame','i_c')*self.dims_temp[0]-cfg.getfloat('FreeFrame','sz')*self.dims_temp[0]/2),int((cfg.getfloat('FreeFrame','i_c')*self.dims_temp[0]+cfg.getfloat('FreeFrame','sz')*self.dims_temp[0]/2))]]
                self.hotspot_j = [[int((cfg.getfloat('FreeFrame','j_c')*self.dims_temp[1]-cfg.getfloat('FreeFrame','sz')*self.dims_temp[0]/2)),int((cfg.getfloat('FreeFrame','j_c')*self.dims_temp[1]+cfg.getfloat('FreeFrame','sz')*self.dims_temp[0]/2))]]
                self.Tspot = cfg.getfloat('FreeFrame','Tspot')
                if self.hotspot_on==0:
                    self.set_hotspot()
            
            #Hotspots initialisation for RealisticFrame       
            else:
                self.n_spot_on = 0
                #Implement hotspots coordinates
                line1 = int((self.outside + self.t + self.b + 5*self.hotspot_space + self.hotspot_dim[0]*7/2)*self.g)
                line2 = int((self.outside + self.t + self.b + 4*self.hotspot_space + self.hotspot_dim[0]*5/2)*self.g)
                line3 = int((self.outside + 2*self.hotspot_space + self.hotspot_dim[0]*3/2)*self.g)
                line4 = int((self.outside + self.hotspot_space + self.hotspot_dim[0]/2)*self.g)
                
                for location in self.dict_hotspot.keys():
                    if self.dict_hotspot[location]['line'] == 1:
                        self.dict_hotspot[location]['coord_i'] = line1
                    elif self.dict_hotspot[location]['line'] == 2:
                        self.dict_hotspot[location]['coord_i'] = line2
                    elif self.dict_hotspot[location]['line'] == 3:
                        self.dict_hotspot[location]['coord_i'] = line3
                    elif self.dict_hotspot[location]['line'] == 4:
                        self.dict_hotspot[location]['coord_i'] = line4
                    col = self.dict_hotspot[location]['column']
                    self.dict_hotspot[location]['coord_j'] = int((self.outside + col*self.hotspot_space + (col- 1/2)*self.hotspot_dim[1])*self.g)    
                # Turn on hotspots
                    if self.dict_hotspot[location]['Temperature'] != -1:
                        self.n_spot_on += 1
                        self.hotspot_i.append([int(self.dict_hotspot[location]['coord_i'] - self.hotspot_dim[0]*self.g/2), int(self.dict_hotspot[location]['coord_i'] + self.hotspot_dim[0]*self.g/2)])
                        self.hotspot_j.append([int(self.dict_hotspot[location]['coord_j'] - self.hotspot_dim[1]*self.g/2), int(self.dict_hotspot[location]['coord_j'] + self.hotspot_dim[1]*self.g/2)])
                        self.Tspot = self.dict_hotspot[location]['Temperature']
                self.set_hotspot()  
        else:
            self.hot_used=False
            self.hot_on=False

        self.tempField_history = [self.tempField]              #History of temperature field at every timestep
        self.beeTempField = self.Tamb*np.ones(self.dims_b) # T° field for bees
        self.Tmax = [self.Tamb]                            # History of max T°
        self.Tcs = [self.Tamb]                            # History of T° at centroid
        self.Tmax_j = [0]                                   # History of j coordinate of max T° position
        self.meanT = [self.Tamb]                           # History of mean T°
        self.sigT = [0]                                     # History of std T°

        #Colony initialisation
        self.n_bees = cfg.getint('hive','n_bees')
        self.beeGrid = np.zeros(self.dims_b)                # Grid of bees
        self.beeGrid_thermo = np.full(self.dims_b, 0)       # Grid of thermogenesis local temperatures
        self.active_bee_list = list()                       #List to contain the number of active bees.
        self.colony = np.asarray(self.init_colony(self.n_bees,cfg.get('hive','init_shape'),cfg['bee'])) #List of bees
        if self.n_bees>0:
            self.centroid = np.mean(np.argwhere(self.beeGrid),axis=0)
        else:
            self.centroid = [0,0]
        self.bgs_history = [self.beeGrid.copy()]

        #2nd layer of beeGrid for bees in 'leave' state
        self.beeGrid_2nd = np.zeros(self.dims_b)
        self.bgs2_history = [self.beeGrid_2nd.copy()]


    def init_colony(self,_n_bees,_init_shape,_bee_param):
        """Build the list of agents (Bee objects) by random draw according to param."""
        self.bee_xmax = self.dims_b[0]-1
        self.bee_ymax = self.dims_b[1]-1
        initBeeBehaviour(_bee_param, self.bee_xmax, self.bee_ymax) # Initialise bee behaviour based on _bee_param
        
        bs = []
        for _ in range(_n_bees):
            if _init_shape=="disc": #initially in disc offset from corner
                offset = (self.dims_b[0]//2,self.dims_b[1]*2//4)
                #offset = (self.dims_b[0],self.dims_b[1])
                r = int(np.sqrt(2*_n_bees//np.pi))*random.random()
                theta = 2*np.pi*random.random()
                i_b = int(r*np.cos(theta))+offset[0]
                j_b = int(r*np.sin(theta))+offset[1]
                iteration = 0
                while i_b < 0 or j_b < 0 or i_b > self.bee_xmax or j_b > self.bee_ymax or self.beeGrid[i_b,j_b]!= FREE:
                    iteration = iteration +1
                    r = int(np.sqrt(2*_n_bees//np.pi))*random.random()
                    if iteration > np.pi*r*r:
                        r = 1.5*r
                    if iteration > 3*np.pi*r*r/2:
                        r = 2*r
                    theta = 2*np.pi*random.random()
                    i_b = int(r*np.cos(theta))+offset[0]
                    j_b = int(r*np.sin(theta))+offset[1]
            elif _init_shape=="ring": #initially in ring in middle
                r = int(np.sqrt(2*_n_bees//np.pi))*random.random()
                theta = 2*np.pi*random.random()
                i_b = int((r+5)*np.cos(theta))+self.dims_b[0]//2
                j_b = int((r+5)*np.sin(theta))+self.dims_b[1]//2
                while self.beeGrid[i_b,j_b]!=FREE or i_b < 0 or j_b < 0:
                    r = int(np.sqrt(2*_n_bees//np.pi))*random.random()
                    theta = 2*np.pi*random.random()
                    i_b = int((r+5)*np.cos(theta))+self.dims_b[0]//2
                    j_b = int((r+5)*np.sin(theta))+self.dims_b[1]//2

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
        self.l_bee = cfg.getfloat('hive','lambda_bee')
        self.l_air = cfg.getfloat('hive','lambda_air')
        self.hq20 = cfg.getfloat('hive','hq20')
        self.gamma = cfg.getfloat('hive','gamma')
        self.RealisticFrame = cfg.getboolean('hotspot','RealisticFrame')
        self.dims_b = list(ast.literal_eval(cfg.get('FreeFrame','dims_b')))
        self.outside = cfg.getfloat('RealisticFrame','outside')
        self.b = cfg.getfloat('RealisticFrame','b')
        self.t = cfg.getfloat('RealisticFrame','t')
        self.bee_surf = cfg.getfloat('RealisticFrame','bee_surf')
        self.hotspot_space = cfg.getfloat('RealisticFrame','hotspot_space')
        self.hotspot_dim = list(ast.literal_eval(cfg.get('RealisticFrame','hotspot_dim')))
        self.dict_Tamb = {key: ast.literal_eval(value) for key, value in cfg['Tamb_dictionnary'].items()}
        
        #Converting cm data in pixels
        if self.RealisticFrame:
            self.hotspot_space = self.convert_cm_to_array(self.hotspot_space)
            self.hotspot_dim[0] = self.convert_cm_to_array(self.hotspot_dim[0])
            self.hotspot_dim[1] = self.convert_cm_to_array(self.hotspot_dim[1])
            self.outside = self.convert_cm_to_array(self.outside)
            self.b = self.convert_cm_to_array(self.b)
            self.t = self.convert_cm_to_array(self.t)

        # Hotspot initialisation
        if cfg.getboolean('hotspot','used'):
            self.hot_used=True
            self.hotspot_i =list()
            self.hotspot_j = list()
            self.hot_on=False
            
            if self.RealisticFrame==False:
                self.hotspot_on=cfg.getint('FreeFrame','on')
                self.hotspot_off=cfg.getint('FreeFrame','off')
                self.n_spot_on = 1
                self.hotspot_i = [[int(cfg.getfloat('FreeFrame','i_c')*self.dims_temp[0] - cfg.getfloat('FreeFrame','sz')*self.dims_temp[0]/2),int((cfg.getfloat('FreeFrame','i_c')*self.dims_temp[0] + cfg.getfloat('FreeFrame','sz')*self.dims_temp[0]/2))]]
                self.hotspot_j = [[int((cfg.getfloat('FreeFrame','j_c')*self.dims_temp[1] - cfg.getfloat('FreeFrame','sz')*self.dims_temp[0]/2)),int((cfg.getfloat('FreeFrame','j_c')*self.dims_temp[1] + cfg.getfloat('FreeFrame','sz')*self.dims_temp[0]/2))]]
                self.Tspot = cfg.getfloat('FreeFrame','Tspot')
                if self.hotspot_on==0:
                    self.set_hotspot()  
            else:
                self.n_spot_on = 0
                #Implement hotspots coordinates
                line1 = int((self.outside + self.t + self.b + 5*self.hotspot_space + self.hotspot_dim[0]*7/2)*self.g)
                line2 = int((self.outside + self.t + self.b + 4*self.hotspot_space + self.hotspot_dim[0]*5/2)*self.g)
                line3 = int((self.outside + 2*self.hotspot_space + self.hotspot_dim[0]*3/2)*self.g)
                line4 = int((self.outside + self.hotspot_space + self.hotspot_dim[0]/2)*self.g)
                for location in self.dict_hotspot.keys():
                    if self.dict_hotspot[location]['line'] == 1:
                        self.dict_hotspot[location]['coord_i'] = line1
                    elif self.dict_hotspot[location]['line'] == 2:
                        self.dict_hotspot[location]['coord_i'] = line2
                    elif self.dict_hotspot[location]['line'] == 3:
                        self.dict_hotspot[location]['coord_i'] = line3
                    elif self.dict_hotspot[location]['line'] == 4:
                        self.dict_hotspot[location]['coord_i'] = line4
                    col = self.dict_hotspot[location]['column']
                    self.dict_hotspot[location]['coord_j'] = int((self.outside + col*self.hotspot_space + (col- 1/2)*self.hotspot_dim[1])*self.g)   
                # Turn on hotspots
                for location in self.dict_hotspot.keys():
                    if self.dict_hotspot[location]['Temperature'] != -1:
                        self.n_spot_on += 1
                        self.hotspot_i.append([int(self.dict_hotspot[location]['coord_i'] - self.hotspot_dim[0]*self.g/2), int(self.dict_hotspot[location]['coord_i'] + self.hotspot_dim[0]*self.g/2)])
                        self.hotspot_j.append([int(self.dict_hotspot[location]['coord_j'] - self.hotspot_dim[1]*self.g/2), int(self.dict_hotspot[location]['coord_j'] + self.hotspot_dim[1]*self.g/2)])
                        self.Tspot = self.dict_hotspot[location]['Temperature']
                self.set_hotspot()
                
        else:
            self.hot_used=False
            self.hot_on=False

    def init_temp(self, count):
        """Update the temperature field only (no agent movement)"""
        for _ in range(1000):
            self.update_temp()
            self.update_temp_border(count)

    def set_hotspot(self):
        """Turn on the hotspot. Sets its area to a fixed temperature."""
        if self.RealisticFrame == False:
            self.hot_on = True
        for a,b in zip(self.hotspot_i,self.hotspot_j):
            self.tempField[a[0]:a[1],b[0]:b[1]] = self.Tspot
                    
    def f(self,i,j, diffusion):
        """Compute the metabolic temperature contribution of the agent at position (i,j).
        Returns 0 if no agent is at this position.
        Returns the agent's thermogenesis temperature if the agent is in the active state and its thermogenesis 
        temperature is higher than diffusion value computed in "test_diff". 
        Returns a boolean value characterizing the agent's shivering state. 
        """
        f_ij = self.hq20*np.exp(self.gamma*(self.beeTempField[i//self.g,j//self.g]-20)) if (self.beeGrid[i//self.g,j//self.g]!=FREE) else 0
        shivering = False
        test_diff = diffusion + self.tempField[i,j]
        
        if self.beeGrid_thermo[i//self.g,j//self.g] != 0 and test_diff<self.beeGrid_thermo[i//self.g,j//self.g]:
            f_ij = self.beeGrid_thermo[i//self.g,j//self.g]
            shivering = True
        # Temperature threshold
        #elif f_ij > self.hq20*np.exp(self.gamma*(self.max_temp-20)):
            #f_ij= self.hq20*np.exp(self.gamma*(self.max_temp-20))   
        return f_ij, shivering
    
    def diff(self, lamdas):
        """Compute the diffusion term in the temperature equation for position (i,j).
            Based on the diffusion equation presented in Sumpter et al. (2000).
        """
        d, d_3D, diffusion,lamdas_aug = np.zeros(self.dims_temp), np.zeros(self.dims_temp), np.zeros(self.dims_temp), np.zeros(self.dims_temp)
        lambdas_isup, lambdas_iinf = np.zeros(self.dims_temp), np.zeros(self.dims_temp)
        lambdas_jsup, lambdas_jinf = np.zeros(self.dims_temp), np.zeros(self.dims_temp)
        tempfield_isup, tempfield_iinf = np.zeros(self.dims_temp), np.zeros(self.dims_temp)
        tempfield_jsup, tempfield_jinf = np.zeros(self.dims_temp), np.zeros(self.dims_temp)
        #Modify the lamda matrix to obtain the same dimension as in the temperature grid
        for i in range(self.dims_temp[0]):
            lamdas_row = np.repeat(lamdas[i//2, :], 2)
            lamdas_aug[i:i+1, :] = lamdas_row
            
        # Compute the matrix characterizing each neighbor
        lambdas_isup = np.roll(lamdas_aug, 1, axis=0)
        lambdas_iinf = np.roll(lamdas_aug, -1, axis=0)
        lambdas_jsup = np.roll(lamdas_aug, 1, axis=1)
        lambdas_jinf = np.roll(lamdas_aug, -1, axis=1)
        
        tempfield_isup = np.roll(self.tempField, 1, axis=0) - self.tempField
        tempfield_iinf = np.roll(self.tempField, -1, axis=0) - self.tempField
        tempfield_jsup = np.roll(self.tempField, 1, axis=1) - self.tempField
        tempfield_jinf = np.roll(self.tempField, -1, axis=1) - self.tempField
        
        neighbors = np.multiply(lambdas_isup, tempfield_isup) + np.multiply(lambdas_iinf, tempfield_iinf) + np.multiply(lambdas_jsup, tempfield_jsup) + np.multiply(lambdas_jinf, tempfield_jinf)
        d_3D= (self.dim_scaling*self.l_air)*(self.Tamb-self.tempField)
        neighbors = neighbors + d_3D
        d = np.multiply(lamdas_aug, neighbors)
        if self.dim_scaling == 0:
            # Diffusion calculated in 2D
            diffusion = d/4
        else:
            # Diffusion calculated in 3D
            diffusion = d/5
        return diffusion

    def h(self,i,j):
        """Checks whether position (i,j) is within the boundaries of the hotspot."""
        for n in range(self.n_spot_on):
            if i>self.hotspot_i[n][0] and i<self.hotspot_i[n][1] and j>self.hotspot_j[n][0] and j<self.hotspot_j[n][1]:
                return n
        return -1
    
    def update_temp(self,lamdas):
        """Update the temperature field."""
        diffusion_term = self.diff(lamdas)
        for i in range(1,self.dims_temp[0] - 1): # Exclude borders because initial condition
            for j in range(1,self.dims_temp[1] - 1):
                if self.hot_on:
                    hotspot= self.h(i,j)
                    if hotspot!= -1:
                        j=self.hotspot_j[hotspot][1] - 1 #Skips all other pixels on the hotspot row
                        continue
                heating, shivering = self.f(i,j, diffusion_term[i,j])
                if shivering == True:
                    self.tempField[i,j] = heating
                else:
                    self.tempField[i,j] += diffusion_term[i,j] + heating
   
    def update_temp_border(self, count):
        """Update the temperature field at the border of the grid."""
        for keys in self.dict_Tamb.keys():
            if self.dict_Tamb[keys]['beginning'] == count:
                self.Tobj = self.dict_Tamb[keys]['Temperature']
        # Equation controling ambient temperature change
        self.Tamb += (self.Tobj - self.Tamb)*self.Kp
        for i in range(self.dims_temp[0]):
            self.tempField[i,0] = self.Tamb
            self.tempField[i,-1] = self.Tamb
        for j in range(self.dims_temp[1]):
            self.tempField[0,j] = self.Tamb
            self.tempField[-1,j] = self.Tamb

    def update(self,count):
        """Update the Frame state. Called at each timestep.
        - count is the iteration number
        """
        
        #Compute the temperature felt by the agents and update them
        self.compute_Tbee()
        idxs = np.arange(self.colony.size)
        np.random.shuffle(idxs)
        for i in idxs:
            self.colony[i].update(self.beeTempField,self.beeGrid,self.beeGrid_2nd, self.beeGrid_thermo, self.n_bees)
            
        if self.RealisticFrame == False:
            if self.hot_used: # Hotspot management
                if self.hotspot_on==count:
                    self.set_hotspot()
                elif self.hot_on and self.hotspot_off==count:
                    self.hot_on = False
        else:
            if self.hot_used: # Hotspot management
                self.set_hotspot()
        if len(self.dict_Tamb)>1:
            self.update_temp_border(count)

        # Tau temperature updates for each bee update
        Pij=(self.beeGrid)%2 # Pij = 1 if a beespot is STAT, 0 if a beespot is FREE or MOV
        lamdas=self.l_air-Pij*(self.l_air-self.l_bee)
        for _ in range(self.tau):
            self.update_temp(lamdas)
        
        # Update measurements of temp history
        self.Tmax.append(np.amax(self.tempField))
        self.Tmax_j.append(np.unravel_index(np.argmax(self.tempField, axis=None), self.tempField.shape)[1]) # j position of max T°
        self.meanT.append(np.mean(self.tempField))
        self.sigT.append(np.std(self.tempField))
        
        #Saving state
        if self.n_bees>0:
            self.centroid = np.mean(np.argwhere(self.beeGrid),axis=0)
        else:
            self.centroid = [0,0]
        self.Tcs.append(self.beeTempField[int(self.centroid[0]),int(self.centroid[1])])
        self.tempField_history.append(self.tempField.copy())
        self.bgs_history.append(self.beeGrid.copy())
        self.bgs2_history.append(self.beeGrid_2nd.copy())
        self.active_bee_list.append(np.count_nonzero(self.beeGrid_thermo))
    
    def compute_Tbee(self):
        """Compute local average of temperature at each possible agent position."""
        #   From https://stackoverflow.com/questions/26871083/how-can-i-vectorize-the-averaging-of-2x2-sub-arrays-of-numpy-array :
        #   Using the reshape method for faster computation
        beeTempField = self.tempField.reshape(np.shape(self.tempField)[0]//2, 2, np.shape(self.tempField)[1]//2, 2)
        self.beeTempField = beeTempField.mean(axis=(1,3))
        
    def convert_cm_to_array(self, cm):
        """Converts a distance in cm to coordinates in bee grid array, based on the volume taken by a bee"""
        pixels = round(cm/np.sqrt(self.bee_surf))
        return pixels