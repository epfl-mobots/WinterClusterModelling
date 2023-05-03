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
        self.direction = np.array([0,0])
        self.bounced = 0
    
    def draw_direction(self, exclude='none'):
        borders = ['up','down','left','right']
        if exclude!='none':
            borders.remove(exclude)
        border = np.random.choice(borders)

        if border=='up':
            self.direction = np.array([0,np.random.randint(self.jmax+1)])
        if border=='down':
            self.direction = np.array([self.imax,np.random.randint(self.jmax+1)])
        if border=='left':
            self.direction = np.array([np.random.randint(self.imax+1),0])
        if border=='right':
            self.direction = np.array([np.random.randint(self.imax+1),self.jmax])
        
        if self.state == 'explore':
            self.bounced += 1
        
    def move_toward_dir(self,beeGrid,init_pos):
        #print("initial position : ",self.i, " ", self.j)
        pos_dir = init_pos + (1/np.linalg.norm(self.direction-init_pos))*(self.direction-init_pos)
        #print("direct_pos : ", pos_dir)

        next_pos = np.array([0,0])
        min_dist = 10000
        for ip,jp in zip([self.i-1,self.i,self.i+1,self.i],[self.j,self.j-1,self.j,self.j+1]):
            if ip>self.imax or jp>self.jmax or beeGrid[ip,jp]!=0:
                continue
            if np.linalg.norm(pos_dir-np.array([ip,jp]))<min_dist:
                next_pos = np.array([ip,jp])
                min_dist = np.linalg.norm(pos_dir-next_pos)
        
        if min_dist!=10000: #if there is a free spot somewhere around that the bee will move to
            self.i = next_pos[0]
            self.j = next_pos[1]

        #print("next_pos : ", [self.i,self.j])

    def update(self,tempField,beeGrid):
        init_pos = np.array([self.i,self.j])
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
            #go back to sumpter if local temp is comfy or if bounced twice
            if (tempField[self.i,self.j]>self.TminI and tempField[self.i,self.j]<self.TmaxI) or self.bounced>=2:
                self.state='sumpter'
                self.bounced = 0

        ## ACTIONS according to state
        if tempField[self.i,self.j]<self.Tcoma:
            return
        
        else:
            beeGrid[self.i,self.j]=0

            if self.state == 'sumpter':
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
                
                '''print("neighbors with appropriate temperature :", xy_TI)
                print("other free neighbor spots : ", xy_free)
                print("temps ", temp_free)
                print("end position : ",self.i, " ", self.j)'''
        
            elif self.state == 'leave' or self.state=='explore':
                # if hit a wall, draw a new direction on another wall
                if self.i == self.imax:
                    self.draw_direction(exclude='down')
                if self.i == 0:
                    self.draw_direction(exclude='up')
                if self.j == self.jmax:
                    self.draw_direction(exclude='right')
                if self.j == 0:
                    self.draw_direction(exclude='left')

                self.move_toward_dir(beeGrid,init_pos)
                
            # update beeGrid with the new position (and if bee is static or moved)
            if self.i==init_pos[0] and self.j==init_pos[1]:
                beeGrid[self.i,self.j]=1
            else:
                beeGrid[self.i,self.j]=2
            
                

