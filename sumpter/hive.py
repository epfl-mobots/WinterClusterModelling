import numpy as np
import random
from bee import Bee

class Hive:
    def __init__(self, param, sim_time,hotspot=False):
        self.param = param
        self.tau = param["tau"]
        self.g = param["g"]
        self.dims_b = param["dims_b"]
        self.l_bee = param["lambda_bee"]
        self.l_air = param["lambda_air"]
        self.hq20 = param["hq20"]
        self.gamma = param["gamma"]

        ##### Temperature field initialization ######################################################
        #self.temp = TempField(param["temp_param"])
        self.dims_temp = param["dims_temp"]
        self.hotspot = hotspot
        if hotspot:
            #computing position of possible hotspots depending on the temperature field dimensions
            self.i_hot = [int(0.1*self.dims_temp[0]),int(0.56*self.dims_temp[0])]
            self.j_hot = [int((0.03+0.4*k)*self.dims_temp[1]) for k in range(5)]
            self.sz_spot = int(0.34*self.dims_temp[0])

            #setting position of hotspot
            self.hotspot = (self.i_hot[param["i_hotspot"]],self.j_hot[param["j_hotspot"]])
            self.Tspot = param['Tspot']

        #preallocating memory to save stuff
        self.tempField_save = np.zeros((sim_time,self.dims_temp[0],self.dims_temp[1]))    
        self.Tmax = np.zeros(sim_time)
        self.Tc = np.zeros(sim_time)
        self.Tmax_j = np.zeros(sim_time)
        self.meanT = np.zeros(sim_time)
        self.sigT = np.zeros(sim_time)
        #initializing data to save
        self.tempField_save[0,:,:] = param['tempA']*np.ones(self.param['dims_temp'])
        self.Tmax[0] = param['tempA']
        self.Tc[0] = param['tempA']
        self.Tmax_j[0] = 0
        self.meanT[0] = param['tempA']
        self.sigT[0] = 0

        self.tempField = param['tempA']*np.ones(self.param['dims_temp'])     
        self.beeTempField = param['tempA']*np.ones(self.param['dims_b'])

        #### Colony initialization ######################################################
        self.beeGrid = np.zeros((sim_time,self.dims_b[0],self.dims_b[1]))

        self.n_bees = param["n_bees"]   
        bs = self.init_colony(param)
        self.colony = np.array(bs)
        self.centroid = np.mean(np.argwhere(self.beeGrid[0]),axis=0)

        #self.init_temp()


    def init_colony(self,param):
        bs = []
        for i in range(param["n_bees"]):
            if param["init_shape"]=="disc":
            # initially in disc offset from corner
                offset = (self.dims_b[0]//2,self.dims_b[1]//2)
                r = 7*random.random()
                theta = 2*np.pi*random.random()
                i_b = int(r*np.cos(theta))+offset[0]
                j_b = int(r*np.sin(theta))+offset[1]
                while self.beeGrid[0][i_b,j_b]!=0:
                    r = 10*random.random()
                    theta = 2*np.pi*random.random()
                    i_b = int(r*np.cos(theta))+offset[0]
                    j_b = int(r*np.sin(theta))+offset[1]

            elif param["init_shape"]=="ring":
                # initially in ring in middle
                r = 7*random.random()
                theta = 2*np.pi*random.random()
                i_b = int((r+2)*np.cos(theta))+self.dims_b[0]//2
                j_b = int((r+2)*np.sin(theta))+self.dims_b[1]//2
                while self.beeGrid[0][i_b,j_b]!=0:
                    r = 10*random.random()
                    theta = 2*np.pi*random.random()
                    i_b = int((r+2)*np.cos(theta))+self.dims_b[0]//2
                    j_b = int((r+2)*np.sin(theta))+self.dims_b[1]//2

            else: # random initialization across grid
                i_b = 1 + int(random.random()*(self.dims_b[0]-2))
                j_b = 1 + int(random.random()*(self.dims_b[1]-2))
                while self.beeGrid[0][i_b,j_b]!=0:
                    i_b = 1 + int(random.random()*(self.dims_b[0]-2))
                    j_b = 1 + int(random.random()*(self.dims_b[1]-2))
            
            self.beeGrid[0][i_b,j_b] = 1
            
            print(i," : ",i_b, ", ",j_b)
            bs.append(Bee(i_b,j_b,param["bee_param"]))
            
        # for i in range(param["n_bees"]):
        #     bs.append(Bee(int(random.random()*self.dims_b[0]),int(random.random()*self.dims_b[1])))
        self.colony = np.array(bs)

        self.init_temp()


    def init_temp(self):
        for _ in range(1000):
            self.update_temp()

    def f(self,count,i,j):
        if ((i%2==0) and (j%2==0) and (self.beeGrid[count-1][i//2,j//2]!=0)):
            return self.hq20*np.exp(self.gamma*(self.tempField[i,j]-20))

        return 0

    def diff(self,count,i,j):
        d = 0
        l = self.l_bee if ((i%2==0) and (j%2==0) and (self.beeGrid[count-1][i//2,j//2]==1)) else self.l_air

        for ip,jp in zip([i-1,i,i+1,i],[j,j-1,j,j+1]):
            lp = self.l_bee if ((ip%2==0) and (jp%2==0) and (self.beeGrid[count-1][ip//2,jp//2]==1)) else self.l_air
            d += l*lp*(self.tempField[ip,jp]-self.tempField[i,j])

        return 0.25*d   

    def update_temp(self,count):
        if self.hotspot:
            self.tempField[self.hotspot[0],self.hotspot[1]] = self.Tspot
        self.tempField[1:self.dims_temp[0]-1,1:self.dims_temp[1]-1] = np.array([[self.tempField[i,j] + self.diff(count,i,j) + self.f(count,i,j) for j in range(1,self.dims_temp[1]-1)] for i in range(1,self.dims_temp[0]-1)])
        # for i in range(1,self.dims_temp[0]-1):
        #     for j in range(1,self.dims_temp[1]-1):
        #         if self.hotspot and (i,j)==self.hotspot:
        #             continue
        #         self.tempField[i,j] += self.diff(count,i,j) + self.f(count,i,j)

    def update(self,count):
        # tau temperature updates for each bee update
        for _ in range(self.tau):
            self.update_temp(count)
        
        # update measurements of temp history
        self.tempField_save[count] = self.tempField
        self.Tmax[count] = np.amax(self.tempField)
        self.Tmax_j[count] = np.unravel_index(np.argmax(self.tempField, axis=None), self.tempField.shape)[1]
        self.meanT[count] = np.mean(self.tempField)
        self.sigT[count] = np.std(self.tempField)

        self.compute_Tbee(count)
        idxs = np.arange(self.colony.size)
        np.random.shuffle(idxs)
        bg = self.beeGrid[count-1].copy() #temporary variable on which the bee's positions will be updated
        for i in idxs:
            self.colony[i].update(self.beeTempField,bg)
        self.beeGrid[count] = bg
        
        self.centroid = np.mean(np.argwhere(self.beeGrid[count]),axis=0)
        self.Tc[count] = self.beeTempField[int(self.centroid[0]),int(self.centroid[1])]
        
    
    def compute_Tbee(self, count):
        for x in range(1,self.dims_b[0]):
            for y in range(1,self.dims_b[1]):
                x_st = int(self.g*(x-0.5))
                x_e = int(self.g*(x+1-0.5))
                y_st = int(self.g*(y-0.5))
                y_e = int(self.g*(y+1-0.5))
                self.beeTempField[x,y] = sum(sum(self.tempField[x_st:x_e,y_st:y_e]))/(self.g**2)
    
    