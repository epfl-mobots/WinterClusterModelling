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
        '''print("initial position : ",self.i, " ", self.j, " ", tempField[self.i,self.j])'''
        init_pos = (self.i,self.j)

        if tempField[self.i,self.j]<self.Tcoma:
            return
        else:
            beeGrid[self.i,self.j]=0
            xy_TI = [] # positions within reachable range that are within [TminI;TmaxI]
            xy_free = [] # other positions within reachable range
            temp_free = []
            for ip,jp in zip([self.i-1,self.i,self.i+1,self.i,self.i],[self.j,self.j-1,self.j,self.j+1,self.j]):
                if jp<1 or jp>self.jmax or ip<1 or ip>self.imax:
                    continue
                if beeGrid[ip,jp]==0:
                    '''print("[",ip,",",jp,"]:",tempField[ip,jp])'''
                    if tempField[ip,jp]<=self.TmaxI and tempField[ip,jp]>=self.TminI:
                        xy_TI.append([ip,jp])
                        '''print(ip," ",jp)'''
                    else:
                        xy_free.append([ip,jp])
                        temp_free.append(abs(tempField[ip,jp]-0.5*(self.TmaxI+self.TminI)))

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
                    '''print("indexes of closest temps : ",idxs)'''
                    if len(idxs)==1:
                        idx = idxs[0][0]
                    else: 
                        idx = idxs[np.random.randint(0,len(idxs))]
                    if temp_free[idx]!=tempField[self.i,self.j]:
                        self.i = xy_free[idx][0]
                        self.j = xy_free[idx][1]
            
            if self.i==init_pos[0] and self.j==init_pos[1]:
                beeGrid[self.i,self.j]=1
            else:
                beeGrid[self.i,self.j]=2
            
            '''print("neighbors with appropriate temperature :", xy_TI)
            print("other free neighbor spots : ", xy_free)
            print("temps ", temp_free)
            print("end position : ",self.i, " ", self.j)'''
            

