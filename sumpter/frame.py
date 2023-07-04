"""Definition of Frame class which handles the agents (Bee objects) and the temperature field."""

import numpy as np
import random
#import sys
#sys.path.append("C:\\Users\\Louise\\Documents\\EPFL\\MA4\\Project\\WinterClusterModelling\\sumpter")
from bee import Bee, FREE, STAT, MOV
import draw
import datetime

class Frame:
    def __init__(self, param, hotspot,graphpath):
        """Initialisation of Frame object
        param : parameters of the temperature field and agents
        hotspot : either False or parameters of the hotspot
        """
        self.graphpath=graphpath
        self.tau = param["tau"]
        self.g = param["g"]
        self.dims_b = param["dims_b"]
        self.l_bee = param["lambda_bee"]
        self.l_air = param["lambda_air"]
        self.hq20 = param["hq20"]
        self.gamma = param["gamma"]

        #temperature field initialization - initially homogenous at ambient temperature
        self.dims_temp = tuple(self.g*dim for dim in self.dims_b)
        self.tempField = param['tempA']*np.ones(self.dims_temp)

        self.hot_on=False
        self.hotspot = hotspot
        if type(self.hotspot)!=bool:
            if hotspot['coord']!=[]:
                #computing position of possible hotspots depending on the temperature field dimensions
                self.i_hot = [int(0.1*self.dims_temp[0]),int(0.56*self.dims_temp[0])]
                self.j_hot = [int((0.03+0.4*k)*self.dims_temp[0]) for k in range(5)]
                self.sz_spot = int(0.34*self.dims_temp[0])

                #setting position of hotspot
                self.n_spot = len(hotspot['coord'])
                self.hotspot_i = [[self.i_hot[i],self.i_hot[i]+self.sz_spot] for [i,_] in hotspot['coord']]#(self.i_hot[param["i_hotspot"]],self.j_hot[param["j_hotspot"]])
                self.hotspot_j = [[self.j_hot[j],self.j_hot[j]+self.sz_spot] for [_,j] in hotspot['coord']]
            else:
                self.n_spot = 1
                self.hotspot_i = [[int((hotspot['i_c']-hotspot['sz']/2)*self.dims_temp[0]),int((hotspot['i_c']+hotspot['sz']/2)*self.dims_temp[0])]]
                self.hotspot_j = [[int((hotspot['j_c']-hotspot['sz']/4)*self.dims_temp[1]),int((hotspot['j_c']+hotspot['sz']/4)*self.dims_temp[1])]]

            self.Tspot = hotspot['Tspot']
            if hotspot['on']==0:
                self.set_hotspot()

        #history of temperature field at every timestep
        self.tempField_save = [self.tempField]

        self.beeTempField = param['tempA']*np.ones(self.dims_b)
        self.Tmax = [param['tempA']]
        self.Tcs = [param['tempA']]
        self.Tmax_j = [0]
        self.meanT = [param['tempA']]
        self.sigT = [0]

        #colony initialisation
        self.n_bees = param["n_bees"]
        self.beeGrid = np.zeros(self.dims_b) # Grid of bees
        self.colony = np.asarray(self.init_colony(param["n_bees"],param["init_shape"],param["bee_param"])) #List of bees
        self.centroid = np.mean(np.argwhere(self.beeGrid),axis=0)
        self.bgs_save = [self.beeGrid.copy()]

        #2nd layer of beeGrid for bees in 'leave' state
        self.beeGrid_2nd = np.zeros(self.dims_b)
        self.bgs2_save = [self.beeGrid_2nd.copy()]

        #initial stage where only the temperature dynamics are active (no agent movement)
        #self.init_temp()


    def init_colony(self,_n_bees,_init_shape,_bee_param):
        """Build the list of agents (Bee objects) by random draw according to param."""
        bs = []
        for _ in range(_n_bees):
            if _init_shape=="disc": #initially in disc offset from corner
                offset = (self.dims_b[0]//2,self.dims_b[1]//4)
                r = 10*int(np.sqrt(_n_bees//100))*random.random()
                theta = 2*np.pi*random.random()
                i_b = int(r*np.cos(theta))+offset[0]
                j_b = int(r*np.sin(theta))+offset[1]
                while self.beeGrid[i_b,j_b]!=FREE:
                    r = 10*random.random()
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
        # if self.tempField[i,j] >35:
        #     print(self.tempField[i,j])
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
        for i in range(1,self.dims_temp[0]-1): # Exclude borders because initial condition
            for j in range(1,self.dims_temp[1]-1):
                if self.hot_on:
                    hotspot= self.h(i,j)
                    if hotspot!=-1:
                        j=self.hotspot_j[hotspot][1]-1 #Skips all other pixels on the hotspot
                        continue
                diffusion_term= self.diff(i,j,lamdas)
                heating = self.f(i,j)
                self.tempField[i,j] += diffusion_term + heating

                if self.tempField[i,j]>100 or self.tempField[i,j]<-100 : 
                    print(f"heating = {heating}")
                    print(f"diffusion = {diffusion_term}")
                    draw.update(self,self.graphpath,599)
                    exit()

    def update(self,count):
        """Update the Frame state. Called at each timestep.
        - count is the iteration number
        """

        if self.hotspot['on']==count:
            self.set_hotspot()
        elif self.hot_on and self.hotspot['off']==count:
            self.hot_on = False

        # tau temperature updates for each bee update
        Pij=(self.beeGrid)%2
        lamdas=self.l_air-Pij*(self.l_air-self.l_bee)
        for _ in range(self.tau):
            self.update_temp(lamdas)
        
        # update measurements of temp history
        self.Tmax.append(np.amax(self.tempField))
        self.Tmax_j.append(np.unravel_index(np.argmax(self.tempField, axis=None), self.tempField.shape)[1]) # Not sure what this is
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