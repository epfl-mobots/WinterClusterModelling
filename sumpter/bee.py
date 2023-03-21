from processing_py import *
import numpy as np

class Bee:
    def __init__(self, x, y, param):
        self.TminI = param["TminI"]
        self.TmaxI = param["TmaxI"]
        self.Tcoma = param["Tcoma"]
        self.x = x
        self.y = y
        self.met_rate = 0
    
    def update(self,tempField,beeGrid):
        if tempField[self.x,self.y]<self.Tcoma:
            return
        else:
            beeGrid[self.x,self.y]=0
            xy_TI = []
            xy_free = []
            for xp in range(self.x-1,self.x+1):
                for yp in range(self.y-1,self.y+1):
                    if beeGrid[xp,yp]==0:
                        if tempField[xp,yp]<=self.TmaxI and tempField[xp,yp]>=self.TminI:
                            xy_TI.append([xp,yp])
                        else:
                            xy_free.append([xp,yp])
            if xy_TI:
                if len(xy_TI)==1:
                    self.x = xy_TI[0][0]
                    self.y = xy_TI[0][1]
                else:
                    idx = np.randint(0,len(xy_TI)-1)
                    self.x = xy_TI[idx][0]
                    self.y = xy_TI[idx][1]
            elif xy_free:
                if len(xy_free)==1:
                    self.x = xy_free[0][0]
                    self.y = xy_free[0][1]
                else:
                    idx = np.randint(0,len(xy_free)-1)
                    self.x = xy_free[idx][0]
                    self.y = xy_free[idx][1]
            beeGrid[self.x,self,y]=1
            

