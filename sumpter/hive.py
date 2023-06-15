"""Definition of Hive class which handles the agents (Bee objects) and the temperature field."""

import numpy as np
import random
import sys
sys.path.append("C:\\Users\\Louise\\Documents\\EPFL\\MA4\\Project\\WinterClusterModelling\\sumpter")
from bee import Bee, FREE, STAT, MOV

class Hive:
    def __init__(self, param, hotspot):
        self.param = param
        self.tau = param["tau"]
        self.g = param["g"]
        self.dims_b = param["dims_b"]
        self.l_bee = param["lambda_bee"]
        self.l_air = param["lambda_air"]
        self.hq20 = param["hq20"]
        self.gamma = param["gamma"]

        #temperature field initialization - initially homogenous at ambient temperature
        self.dims_temp = param["dims_temp"]
        self.tempField = param['tempA']*np.ones(self.param['dims_temp'])

        self.hot_on=False
        self.hotspot = hotspot
        if type(hotspot)!=bool:
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

        self.beeTempField = param['tempA']*np.ones(self.param['dims_b'])
        self.Tmax = [param['tempA']]
        self.Tc = [param['tempA']]
        self.Tmax_j = [0]
        self.meanT = [param['tempA']]
        self.sigT = [0]

        #colony initialization
        self.n_bees = param["n_bees"]
        self.beeGrid = np.zeros(self.dims_b)
        bs = self.init_colony(param)
        self.colony = np.array(bs)
        self.centroid = np.mean(np.argwhere(self.beeGrid),axis=0)
        self.bg_save = [self.beeGrid.copy()]

        #2nd layer of beeGrid for bees in 'leave' state
        self.beeGrid_2nd = np.zeros(self.dims_b)
        self.bg2_save = [self.beeGrid_2nd.copy()]

        #initial stage where only the temperature dynamics are active (no agent movement)
        #self.init_temp()


    def init_colony(self,param):
        bs = []
        for i in range(param["n_bees"]):
            if param["init_shape"]=="disc": #initially in disc offset from corner
                offset = (self.dims_b[0]//2,self.dims_b[1]//4)
                r = 7*int(np.sqrt(param["n_bees"]//200))*random.random()
                theta = 2*np.pi*random.random()
                i_b = int(r*np.cos(theta))+offset[0]
                j_b = int(r*np.sin(theta))+offset[1]
                while self.beeGrid[i_b,j_b]!=FREE:
                    r = 10*random.random()
                    theta = 2*np.pi*random.random()
                    i_b = int(r*np.cos(theta))+offset[0]
                    j_b = int(r*np.sin(theta))+offset[1]

            elif param["init_shape"]=="ring": #initially in ring in middle
                r = 7*random.random()
                theta = 2*np.pi*random.random()
                i_b = int((r+2)*np.cos(theta))+self.dims_b[0]//2
                j_b = int((r+2)*np.sin(theta))+self.dims_b[1]//2
                while self.beeGrid[i_b,j_b]!=FREE:
                    r = 10*random.random()
                    theta = 2*np.pi*random.random()
                    i_b = int((r+2)*np.cos(theta))+self.dims_b[0]//2
                    j_b = int((r+2)*np.sin(theta))+self.dims_b[1]//2

            else: #random initialization across grid
                i_b = 1 + int(random.random()*(self.dims_b[0]-2))
                j_b = 1 + int(random.random()*(self.dims_b[1]-2)//2)
                while self.beeGrid[i_b,j_b]!=FREE:
                    i_b = 1 + int(random.random()*(self.dims_b[0]-2))
                    j_b = 1 + int(random.random()*(self.dims_b[1]-2)//2)
            
            self.beeGrid[i_b,j_b] = STAT        
            bs.append(Bee(i_b,j_b,param["bee_param"]))
        return bs

    def init_temp(self):
        for _ in range(1000):
            self.update_temp()

    def set_hotspot(self):
        self.hot_on = True
        for a,b in zip(self.hotspot_i,self.hotspot_j):
            self.tempField[a[0]:a[1],b[0]:b[1]] = self.Tspot

    def f(self,i,j):
        if ((i%2==0) and (j%2==0) and (self.beeGrid[i//2,j//2]!=FREE)):
            return self.hq20*np.exp(self.gamma*(self.tempField[i,j]-20))

        return 0

    def diff(self,i,j):
        d = 0
        l = self.l_bee if ((i%2==0) and (j%2==0) and (self.beeGrid[i//2,j//2]==STAT)) else self.l_air

        for ip,jp in zip([i-1,i,i+1,i],[j,j-1,j,j+1]):
            lp = self.l_bee if ((ip%2==0) and (jp%2==0) and (self.beeGrid[ip//2,jp//2]==STAT)) else self.l_air
            d += l*lp*(self.tempField[ip,jp]-self.tempField[i,j])

        return 0.25*d   

    def h(self,i,j):
        for n in range(self.n_spot):
            if i>self.hotspot_i[n][0] and i<self.hotspot_i[n][1] and j>self.hotspot_j[n][0] and j<self.hotspot_j[n][1]:
                return True
        return False

    def update_temp(self):
        # if self.hotspot:
        #     self.tempField[self.hotspot[0],self.hotspot[1]] = self.Tspot
        f_mat = self.hq20*np.exp(self.gamma*(self.tempField-20))
        for i in range(1,self.dims_temp[0]-1):
            for j in range(1,self.dims_temp[1]-1):
                if self.hot_on and self.h(i,j):
                    continue
                f_ij = f_mat[i,j] if ((i%2==0) and (j%2==0) and (self.beeGrid[i//2,j//2]!=FREE)) else 0
                self.tempField[i,j] += self.diff(i,j) + f_ij #+ self.f(i,j)

    def update(self,count):
        if self.hotspot['on']==count:
            self.set_hotspot()
        elif self.hot_on and self.hotspot['off']==count:
            self.hot_on = False

        # tau temperature updates for each bee update
        for _ in range(self.tau):
            self.update_temp()
        
        # update measurements of temp history
        self.Tmax.append(np.amax(self.tempField))
        self.Tmax_j.append(np.unravel_index(np.argmax(self.tempField, axis=None), self.tempField.shape)[1])
        self.meanT.append(np.mean(self.tempField))
        self.sigT.append(np.std(self.tempField))

        self.compute_Tbee()
        idxs = np.arange(self.colony.size)
        np.random.shuffle(idxs)
        for i in idxs:
            self.colony[i].update(self.beeTempField,self.beeGrid,self.beeGrid_2nd)
        
        self.centroid = np.mean(np.argwhere(self.beeGrid),axis=0)
        self.Tc.append(self.beeTempField[int(self.centroid[0]),int(self.centroid[1])])
        self.tempField_save.append(self.tempField.copy())
        self.bg_save.append(self.beeGrid.copy())
        self.bg2_save.append(self.beeGrid_2nd.copy())
        
    
    def compute_Tbee(self):
        for x in range(1,self.dims_b[0]):
            for y in range(1,self.dims_b[1]):
                x_st = int(self.g*(x-0.5))
                x_e = int(self.g*(x+1-0.5))
                y_st = int(self.g*(y-0.5))
                y_e = int(self.g*(y+1-0.5))
                self.beeTempField[x,y] = sum(sum(self.tempField[x_st:x_e,y_st:y_e]))/(self.g**2)
    
    