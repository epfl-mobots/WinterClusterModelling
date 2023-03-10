from processing_py import *
import time

from hive import Hive
from temp_field import TempField
import draw

dims_draw = [800,800]
dims_b = [50,50]
dims_temp = [500,500] #to check if there is a value in paper

class Sim:
    def __init__(self,dims_draw,dims_hive,dims_temp,tempA=12, n_bees=100):
        self.hive = Hive(n_bees, dims_hive, dims_temp,tempA)
        self.app = App(dims_draw[0],dims_draw[1])
        self.start_graphic()
    
    def start_graphic(self):
        draw.init_world(self.app)
        draw.init_temp(self.app,self.hive)
        draw.init_colony(self.app,self.hive)

    def update(self):
        self.hive.update()
        draw.update(self.hive)
    
    def end(self):
        self.app.exit()


sim = Sim(dims_draw,dims_b,dims_temp,12)
time.sleep(15)
sim.end()
