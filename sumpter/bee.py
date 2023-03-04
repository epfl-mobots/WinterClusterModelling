from processing_py import *

class Bee:
    def __init__(self, x, y, t_min=18, t_max=23, t_coma= 8):
        self.t_minI = t_min
        self.t_maxI = t_max
        self.t_chill = t_coma
        self.x = x
        self.y = y
        self.met_rate = 0

