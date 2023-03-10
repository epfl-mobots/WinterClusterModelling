import numpy as np
import random
from bee import Bee
from temp_field import TempField

class Hive:
    def __init__(self, n_bees, dims=[50,50], dimsT=[100,100], tempA=12):
        bs = []
        for i in range(n_bees):
            bs.append(Bee(int(random.random()*dims[0]),int(random.random()*dims[1])))

        self.colony = np.array(bs)
        self.dims_b = dims

        self.temp = TempField(dimsT, tempA)
    
    def update(self):
        self.temp.update(self.colony)
        for b in self.colony:
            b.update()
    