import numpy as np
import random
from bee import Bee
from temp_field import TempField

class Hive:
    def __init__(self, param):
        self.tau = param["tau"]
        self.g = param["g"]
        self.dims_b = param["dims_b"]

        #temperature field initialization
        self.temp = TempField(param["temp_param"])
        self.Tbees = np.ndarray(self.dims_b)
        #bee initialization
        bs = []
        for i in range(param["n_bees"]):
            x = int(self.dims_b[0]/10+self.dims_b[0]/2+i)
            y = int(self.dims_b[1]/10+self.dims_b[1]/2+i)
            print(i," : ",x, ", ",y)
            bs.append(Bee(x,y,param["bee_param"]))
        # for i in range(param["n_bees"]):
        #     bs.append(Bee(int(random.random()*self.dims_b[0]),int(random.random()*self.dims_b[1])))
        self.colony = np.array(bs)
    
    def update(self):
        for t in range(self.tau):
            self.temp.update(self.colony)
        for b in self.colony:
            temp = self.compute_Tbee(b.x,b.y)
            b.update(temp)
    
    def compute_Tbee(self,x,y):
        return sum(self.temp.field[self.g*x:self.g*(x+1),self.g*y:self.g*(y+1)],'all')
    
    