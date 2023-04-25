import numpy as np
import random
from bee import Bee


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

        #temperature field initialization
        #self.temp = TempField(param["temp_param"])
        self.dims_temp = param["dims_temp"]
        self.tempField = param['tempA']*np.ones(self.param['dims_temp'])

        self.hot_on=False
        self.hotspot = hotspot
        if type(hotspot)!=bool:
            #computing position of possible hotspots depending on the temperature field dimensions
            self.i_hot = [int(0.1*self.dims_temp[0]),int(0.56*self.dims_temp[0])]
            self.j_hot = [int((0.03+0.4*k)*self.dims_temp[0]) for k in range(5)]
            self.sz_spot = int(0.34*self.dims_temp[0])

            #setting position of hotspot
            self.n_spot = len(hotspot['coord'])
            self.hotspot_i = [[self.i_hot[i],self.i_hot[i]+self.sz_spot] for [i,_] in hotspot['coord']]#(self.i_hot[param["i_hotspot"]],self.j_hot[param["j_hotspot"]])
            self.hotspot_j = [[self.j_hot[j],self.j_hot[j]+self.sz_spot] for [_,j] in hotspot['coord']]
            self.Tspot = hotspot['Tspot']
            if hotspot['on']==0:
                self.set_hotspot()

                
        
        self.tempField_save = [self.tempField]

        self.beeTempField = param['tempA']*np.ones(self.param['dims_b'])
        self.Tmax = [param['tempA']]
        self.Tc = [param['tempA']]
        self.Tmax_j = [0]
        self.meanT = [param['tempA']]
        self.sigT = [0]

        #colony initialization
        self.n_bees = param["n_bees"]
        self.beeGrid = [np.zeros(self.dims_b)]   
        bs = self.init_colony(param)
        self.colony = np.array(bs)
        self.centroid = np.mean(np.argwhere(self.beeGrid[-1]),axis=0)
        self.bg_save = [self.beeGrid[-1].copy()]
        #self.init_temp()


    def init_colony(self,param):
        bs = []
        for i in range(param["n_bees"]):
            if param["init_shape"]=="disc": # initially in disc offset from corner
                offset = (self.dims_b[0]//2,self.dims_b[1]//4)
                r = 7*random.random()
                theta = 2*np.pi*random.random()
                i_b = int(r*np.cos(theta))+offset[0]
                j_b = int(r*np.sin(theta))+offset[1]
                while self.beeGrid[-1][i_b,j_b]!=0:
                    r = 10*random.random()
                    theta = 2*np.pi*random.random()
                    i_b = int(r*np.cos(theta))+offset[0]
                    j_b = int(r*np.sin(theta))+offset[1]

            elif param["init_shape"]=="ring": # initially in ring in middle
                r = 7*random.random()
                theta = 2*np.pi*random.random()
                i_b = int((r+2)*np.cos(theta))+self.dims_b[0]//2
                j_b = int((r+2)*np.sin(theta))+self.dims_b[1]//2
                while self.beeGrid[-1][i_b,j_b]!=0:
                    r = 10*random.random()
                    theta = 2*np.pi*random.random()
                    i_b = int((r+2)*np.cos(theta))+self.dims_b[0]//2
                    j_b = int((r+2)*np.sin(theta))+self.dims_b[1]//2

            else: # random initialization across grid
                i_b = 1 + int(random.random()*(self.dims_b[0]-2))
                j_b = 1 + int(random.random()*(self.dims_b[1]-2)//2)
                while self.beeGrid[-1][i_b,j_b]!=0:
                    i_b = 1 + int(random.random()*(self.dims_b[0]-2))
                    j_b = 1 + int(random.random()*(self.dims_b[1]-2)//2)
            
            self.beeGrid[-1][i_b,j_b] = 1
            
            # print(i," : ",i_b, ", ",j_b)
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
        if ((i%2==0) and (j%2==0) and (self.beeGrid[-1][i//2,j//2]!=0)):
            return self.hq20*np.exp(self.gamma*(self.tempField[i,j]-20))

        return 0

    def diff(self,i,j):
        d = 0
        l = self.l_bee if ((i%2==0) and (j%2==0) and (self.beeGrid[-1][i//2,j//2]==1)) else self.l_air

        for ip,jp in zip([i-1,i,i+1,i],[j,j-1,j,j+1]):
            lp = self.l_bee if ((ip%2==0) and (jp%2==0) and (self.beeGrid[-1][ip//2,jp//2]==1)) else self.l_air
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
        for i in range(1,self.dims_temp[0]-1):
            for j in range(1,self.dims_temp[1]-1):
                if self.hot_on and self.h(i,j):
                    continue
                self.tempField[i,j] += self.diff(i,j) + self.f(i,j)

    def update(self,count):
        if self.hotspot['on']==count:
            self.set_hotspot()

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
            self.colony[i].update(self.beeTempField,self.beeGrid[-1])
        
        self.centroid = np.mean(np.argwhere(self.beeGrid[-1]),axis=0)
        self.Tc.append(self.beeTempField[int(self.centroid[0]),int(self.centroid[1])])
        self.tempField_save.append(self.tempField.copy())
        self.bg_save.append(self.beeGrid[-1].copy())
        
    
    def compute_Tbee(self):
        for x in range(1,self.dims_b[0]):
            for y in range(1,self.dims_b[1]):
                x_st = int(self.g*(x-0.5))
                x_e = int(self.g*(x+1-0.5))
                y_st = int(self.g*(y-0.5))
                y_e = int(self.g*(y+1-0.5))
                self.beeTempField[x,y] = sum(sum(self.tempField[x_st:x_e,y_st:y_e]))/(self.g**2)
    
    