import numpy as np
import random
from bee import Bee

class Hive:
    def __init__(self, n_bees, dims):
        bs = []
        for i in range(n_bees):
            bs.append(Bee(random.random()*dims[0],random.random()*dims[1]))

        self.bees = np.array(bs)

    