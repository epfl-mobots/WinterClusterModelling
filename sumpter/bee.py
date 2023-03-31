from processing_py import *
import numpy as np

class Bee:
    def __init__(self, x, y, param):
        self.TminI = param["TminI"]
        self.TmaxI = param["TmaxI"]
        self.Tcoma = param["Tcoma"]
        self.imax = param['xmax']
        self.jmax = param['ymax']
        self.i = x
        self.j = y
        self.met_rate = 0
    

    def update(self,tempField,beeGrid):
        # print("initial position : ",self.i, " ", self.j, " ", tempField[self.i,self.j])
        if tempField[self.i,self.j]<self.Tcoma:
            return
        else:
            beeGrid[self.i,self.j]=0
            xy_TI = []
            xy_free = []
            temp_free = []
            for xp,yp in zip([self.i-1,self.i,self.i+1,self.i],[self.j,self.j-1,self.j,self.j+1]):
                if yp<1 or yp>self.jmax or xp<1 or xp>self.imax:
                    continue
                if beeGrid[xp,yp]==0 and not(xp==self.i and yp==self.j):
                    # print("[",xp,",",yp,"]:",tempField[xp,yp])
                    if tempField[xp,yp]<=self.TmaxI and tempField[xp,yp]>=self.TminI:
                        xy_TI.append([xp,yp])
                        #print(xp," ",yp)
                    else:
                        xy_free.append([xp,yp])
                        temp_free.append(abs(tempField[xp,yp]-0.5*(self.TmaxI+self.TminI)))
            if xy_TI:
                if len(xy_TI)==1:
                    self.i = xy_TI[0][0]
                    self.j = xy_TI[0][1]
                else:
                    idx = np.random.randint(0,len(xy_TI))
                    self.i = xy_TI[idx][0]
                    self.j = xy_TI[idx][1]
            elif xy_free:
                if len(xy_free)==1:
                    self.i = xy_free[0][0]
                    self.j = xy_free[0][1]
                else:
                    idxs = np.where(temp_free==min(temp_free))
                    #print("indexes of closest temps : ",idxs)
                    if len(idxs)==1:
                        idx = idxs[0][0]
                    else: 
                        idx = idxs[np.random.randint(0,len(idxs))]
                    if temp_free[idx]!=tempField[self.i,self.j]:
                        self.i = xy_free[idx][0]
                        self.j = xy_free[idx][1]
            beeGrid[self.i,self.j]=1
            
            # print("neighbors with appropriate temperature :", xy_TI)
            # print("other free neighbor spots : ", xy_free)
            # print("temps ", temp_free)
            # print("end position : ",self.i, " ", self.j)
            

