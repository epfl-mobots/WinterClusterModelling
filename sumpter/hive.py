import numpy as np
import random
from bee import Bee
from temp_field import TempField

class Hive:
    def __init__(self, param):
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
        self.tempField = param['tempA']*np.ones(self.param['dims_temp'])
        self.dims_temp = param["dims_temp"]
        
        self.beeTempField = param['tempA']*np.ones(self.param['dims_b'])

        #bee initialization
        self.beeGrid = np.zeros(self.dims_b)
        bs = []
        for i in range(param["n_bees"]):
            r = 7*random.random()
            theta = 2*np.pi*random.random()
            x = int(r*np.cos(theta))+self.dims_b[0]//2
            y = int(r*np.sin(theta))+self.dims_b[1]//2
            while self.beeGrid[x,y]!=0:
                r = 10*random.random()
                theta = 2*np.pi*random.random()
                x = int(r*np.cos(theta))+self.dims_b[0]//2
                y = int(r*np.sin(theta))+self.dims_b[1]//2

            '''x = int(random.random()*self.dims_b[0])
            y = int(random.random()*self.dims_b[1])
            while self.beeGrid[x,y]!=0:
                x = int(random.random()*self.dims_b[0])
                y = int(random.random()*self.dims_b[1])'''
            
            self.beeGrid[x,y] = 1
            
            print(i," : ",x, ", ",y)
            bs.append(Bee(x,y,param["bee_param"]))
            
        # for i in range(param["n_bees"]):
        #     bs.append(Bee(int(random.random()*self.dims_b[0]),int(random.random()*self.dims_b[1])))
        self.colony = np.array(bs)

    def f(self,i,j):
        if ((i%2==0) and (j%2==0) and (self.beeGrid[i//2,j//2]!=0)):
            return self.hq20*np.exp(self.gamma*(self.tempField[i,j]-20))

        return 0

    def diff(self,i,j):
        d = 0

        l = self.l_bee if ((i%2==0) and (j%2==0) and (self.beeGrid[i//2,j//2]!=0)) else self.l_air

        for ip,jp in zip([i-1,i,i+1,i],[j,j-1,j,j+1]):
            lp = self.l_bee if ((ip%2==0) and (jp%2==0) and (self.beeGrid[ip//2,jp//2]!=0)) else self.l_air
            d += l*lp*(self.tempField[ip,jp]-self.tempField[i,j])

        return 0.25*d   

    def update_temp(self):
        for i in range(1,self.dims_temp[0]-1):
            for j in range(1,self.dims_temp[1]-1):
                self.tempField[i,j] += self.diff(i,j) + self.f(i,j)

    def update(self):
        for t in range(self.tau):
            self.update_temp()
        self.compute_Tbee()
        for b in self.colony:
            b.update(self.beeTempField,self.beeGrid)
    
    def compute_Tbee(self):
        for x in range(1,self.dims_b[0]-1):
            for y in range(1,self.dims_b[1]-1):
                self.beeTempField[x,y] = sum(self.tempField[self.g*x:self.g*(x+1),self.g*y:self.g*(y+1)])
    
    