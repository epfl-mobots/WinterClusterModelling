from processing_py import *

class Bee:
    def __init__(self, x, y, param):
        self.TminI = param["TminI"]
        self.TmaxI = param["TmaxI"]
        self.Tcoma = param["Tcoma"]
        self.x = x
        self.y = y
        self.met_rate = 0
    
    def update(self):
        return

