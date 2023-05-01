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

        #states (sumpter - leave - explore)
        self.state = 'sumpter'
        self.prob_tr = param['alpha']
        self.direction = [0,0]
    
    def draw_direction(self):
        border = np.random.choice(['up','down','left','right'])
        if border=='up':
            self.direction = [0,np.random.randint(self.jmax+1)]
        if border=='down':
            self.direction = [self.imax,np.random.randint(self.jmax+1)]
        if border=='left':
            self.direction = [np.random.randint(self.imax+1,0)]
        if border=='right':
            self.direction = [np.random.randint(self.imax+1,self.jmax)]
        

    def update(self,tempField,beeGrid):
        init_pos = (self.i,self.j)
        '''print("initial position : ",self.i, " ", self.j, " ", tempField[self.i,self.j])'''

        #STATE RE_EVALUATION
        if self.state=='sumpter':
            #random draw with a probability prob_tr to go into leave mode
            leave = np.random.choice([True,False],p=[self.prob_tr,1-self.prob_tr])
            if leave:
                self.state = 'leave'
                self.draw_direction()

        elif self.state=='leave':
            #check if neighbouring spots are empty (if they are, leaving phase is over)
            nb_empty=0
            for ip,jp in zip([self.i-1,self.i,self.i+1,self.i],[self.j,self.j-1,self.j,self.j+1]):
                if beeGrid[ip,jp]==0:
                    nb_empty+=1
            if nb_empty==4:
                self.state='explore'

        elif self.state=='explore':
            #check local temperature
            if tempField[self.i,self.j]>self.TminI and tempField[self.i,self.j]<self.TmaxI:
                self.state='sumpter'
            #add implementation for 2 walls hit -> sumpter 

        ## ACTIONS according to state
        if self.state == 'sumpter':
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
        
                

