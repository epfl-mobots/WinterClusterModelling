"""Defines the Bee class (agent class)."""

import numpy as np
import ast
import math

# constants describing the beeGrid state
FREE = 0
STAT = 1
MOV = 2

def initBeeBehaviour(_bee_param, bee_xmax, bee_ymax):
    """Initialise the bee behaviour parameters from the config file given as argument."""
    Bee.TminI = float(_bee_param["TminI"])
    Bee.TmaxI = float(_bee_param["TmaxI"])
    Bee.Tcoma = float(_bee_param["Tcoma"])

    #limits of the terrain
    Bee.imax = bee_xmax
    Bee.jmax = bee_ymax
    
    Bee.BH = _bee_param['BH']

    if Bee.BH == 'explorer':
        Bee.trans_mode = _bee_param['trans_mode']
        Bee.prob_tr = float(_bee_param['alpha'])
        Bee.max_bounce = int(_bee_param['max_bounce'])
        
    Bee.Thermogenese = bool(_bee_param["Thermogenese"])
    if Bee.Thermogenese == True :
        Bee.activate_params = list(ast.literal_eval(_bee_param["activate_params"]))
        Bee.proba_temp_params = list(ast.literal_eval(_bee_param["proba_temp_params"]))
        Bee.prob_deactivate = float(_bee_param['alpha_deactivate'])
        Bee.iter_activate = float(_bee_param['iter_activate'])

class Bee:
    """Class describing the bee agent."""
    def __init__(self, x, y, param):
        """Initialisation of an agent
        x : i coordinate
        y : j coordinate
        param : agent characteristics (described in main.py)
        """

        #position
        self.i = x
        self.j = y

        self.state = 'sumpter' #initial state for both sumpter and explorer BH
        self.thermogenesis = False #initially no thermogenesis
        self.thermo_iter = 0
        
        if Bee.BH == 'explorer':
            self.direction = np.array([0,0])
            self.bounced = 0
    

    def draw_direction(self, bounced, exclude='none'):
        """Compute new target point for the agent movement.
        - exclude can be 'none' or one of the borders. Points from this border are excluded from the draw.
        """
        borders = ['up','down','left','right']
        if exclude!='none':
            borders.remove(exclude)
            if exclude=='up' or exclude=='down':
                border = np.random.choice(borders,p=[1/2,1/4,1/4])
            else:
                border = np.random.choice(borders,p=[2/5,2/5,1/5])
        else:
            border = np.random.choice(borders,p=[1/3,1/3,1/6,1/6])

        # Draw a point on the chosen border
        if border=='up':
            self.direction = np.array([0,np.random.randint(self.jmax+1)])
        if border=='down':
            self.direction = np.array([self.imax,np.random.randint(self.jmax+1)])
        if border=='left':
            self.direction = np.array([np.random.randint(self.imax+1),0])
        if border=='right':
            self.direction = np.array([np.random.randint(self.imax+1),self.jmax])
        
        #Update bounce counter for exploratory BH
        if bounced:
            self.bounced += 1
        
    def move_toward_dir(self,beeGrid,init_pos):
        pos_dir = init_pos + (1/np.linalg.norm(self.direction-init_pos))*(self.direction-init_pos)

        next_pos = np.array([0,0])
        min_dist = 10000
        for ip,jp in zip([self.i-1,self.i,self.i+1,self.i],[self.j,self.j-1,self.j,self.j+1]):
            if ip>self.imax or jp>self.jmax or beeGrid[ip,jp]!=FREE:
                #cannot go out of the grid or pass on top of another bee
                continue
            if np.linalg.norm(pos_dir-np.array([ip,jp]))<min_dist:
                next_pos = np.array([ip,jp])
                min_dist = np.linalg.norm(pos_dir-next_pos)
        
        if min_dist!=10000: #if there is a free spot somewhere around that the bee will move to
            self.i = next_pos[0]
            self.j = next_pos[1]
    
    def compute_leave_prob(self, temp):
        """Compute the probability of an agent to go from 'sumpter' to 'leave' mode based on temp or not."""
        if Bee.trans_mode == 'temp_dep':
            return Bee.prob_tr/(1+math.exp(-0.5*(temp-self.TminI)))
        else:
            return Bee.prob_tr
    
    def compute_prob_activate(self, tempField, beeGrid_thermo, n_bees):
        """Compute the probability of an agent starting thermogenesis shivering based on the ratio
        between its local temperature and the maximum temperature inside the field."""
        if np.max(tempField) == tempField[0,0] or abs(tempField[self.i,self.j]-tempField[0,0])<10^(-10):
            ratio_temp = 0
        else:
            ratio_temp = (tempField[self.i,self.j] - tempField[0,0])/(np.max(tempField)-tempField[0,0])

        proba_activate = Bee.activate_params[0]*np.exp(Bee.activate_params[1]*ratio_temp)
        
        # Set NAN exceptions to zeros
        if math.isnan(proba_activate):
            proba_activate = 0

        return proba_activate
    
    def compute_activate_temp(self):
        """Compute the shivering temperature based on a probability distribution 
        approximating the shivering presented in Stabentheiner 2003.
        Method inspired from: https://stackoverflow.com/questions/66874819/random-numbers-with-user-defined-continuous-probability-distribution 
        """
        
        temp = np.random.uniform(0.5,9)
        y = np.random.uniform(0,0.5)
        proba_temp = Bee.proba_temp_params[0]*np.exp(Bee.proba_temp_params[1]*temp)
        while y>proba_temp:
            temp = np.random.uniform(0.5,9)
            y = np.random.uniform(0,0.0005)
            proba_temp = Bee.proba_temp_params[0]*np.exp(Bee.proba_temp_params[1]*temp)
        return temp
        
    
    def compute_thermogenesis(self, beeGrid_thermo, tempField, n_bees):
        """ Update of the agent thermogenesis state."""    
        if self.thermogenesis == False:
            self.proba_activate = self.compute_prob_activate(tempField, beeGrid_thermo, n_bees)
            #Random draw with a probability proba_activate to enter thermogenesis state
            active = np.random.choice([True,False],p=[self.proba_activate,1-self.proba_activate])
            if active:
                # Agent enters in thermogenesis (active) state.
                self.thermogenesis = True
                # Computation of the local field temperature at the agent's position considering thermogenesis. 
                # This thermogenesis temperature will stay constant until the agent leaves the thermogenesis state.
                self.activate_temp = self.compute_activate_temp() + tempField[self.i,self.j]
                beeGrid_thermo[self.i,self.j] = self.activate_temp 
                
        if self.thermogenesis == True:
            self.thermo_iter = self.thermo_iter + 1
            if self.thermo_iter >= self.iter_activate:
                #Random draw with a probability prob_deactivate to leave thermogenesis state
                deactive = np.random.choice([True,False],p=[self.prob_deactivate,1-self.prob_deactivate])
                if deactive:
                    # Agent enters in passive state.
                    self.thermogenesis = False
                    self.thermo_iter = 0
                else:
                    beeGrid_thermo[self.i,self.j] = self.activate_temp
    def update(self,tempField,beeGrid,beeGrid_2nd, beeGrid_thermo, n_bees):
        """Update of the agent state and position."""
        if tempField[self.i,self.j]<Bee.Tcoma:
            return
        
        init_pos = np.array([self.i,self.j])


        # Behviour from the different BH:
        if Bee.BH == 'explorer':
            #Perform potential state switching
            if self.state=='sumpter' and beeGrid_2nd[self.i,self.j]==FREE:
                leave_prob = self.compute_leave_prob(tempField[self.i,self.j])
                #random draw with a probability leave_prob to go into leave mode
                leave = np.random.choice([True,False],p=[leave_prob,1-leave_prob])
                if leave: #if the bee 'wants' to leave
                    self.state = 'leave'
                    self.draw_direction(bounced=False)

            elif self.state=='leave':
                #check if neighbouring spots are empty (if they are, leaving phase is over)
                nb_empty=0
                for ip,jp in zip([self.i-1,self.i,self.i+1,self.i,self.i],[self.j,self.j-1,self.j,self.j+1,self.j]):
                    if jp<1 or jp>self.jmax or ip<1 or ip>self.imax:
                        continue
                    if beeGrid[ip,jp]==FREE:
                        nb_empty+=1
                if nb_empty==5: #if the spot the bee is in + neighbours are free in 1st layer of bees
                    self.state='explore'

            elif self.state=='explore':
                #go back to sumpter if local temp is comfy or if bounced twice
                if (tempField[self.i,self.j]>self.TminI and tempField[self.i,self.j]<self.TmaxI) or self.bounced>Bee.max_bounce:
                    beeGrid[self.i,self.j]=MOV # move the bee "down"
                    beeGrid_2nd[self.i,self.j]=FREE # free the spot in the 2nd ('leave') layer
                    self.state='sumpter'
                    self.bounced = 0

        ## ACTIONS according to state
        if self.state == 'sumpter':
            beeGrid[self.i,self.j]=FREE
            beeGrid_thermo[self.i,self.j] = 0

            xy_TI = [] # positions within reachable range that are within [TminI;TmaxI]
            xy_free = [] # other positions within reachable range
            temp_free = []
            for ip,jp in zip([self.i-1,self.i,self.i+1,self.i,self.i],[self.j,self.j-1,self.j,self.j+1,self.j]):
                if jp<0 or jp>self.jmax or ip<0 or ip>self.imax:
                    continue
                if beeGrid[ip,jp]==FREE:
                    if tempField[ip,jp]<=self.TmaxI and tempField[ip,jp]>=self.TminI:
                        xy_TI.append([ip,jp])
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
                    if len(idxs)==1:
                        idx = idxs[0][0]
                    else: 
                        idx = idxs[np.random.randint(0,len(idxs))]
                    if temp_free[idx]!=tempField[self.i,self.j]:
                        self.i = xy_free[idx][0]
                        self.j = xy_free[idx][1]
            
            if Bee.Thermogenese == True:
                self.compute_thermogenesis(beeGrid_thermo, tempField, n_bees)
            
            # update beeGrid with the new position (and if bee is static or moved)
            if self.i==init_pos[0] and self.j==init_pos[1]:
                beeGrid[self.i,self.j]=STAT
            else:
                beeGrid[self.i,self.j]=MOV
    
        elif self.state == 'leave':
            if beeGrid_2nd[self.i,self.j]==FREE: #if the bee is not on the 2nd layer
                beeGrid[self.i,self.j]=FREE # move the bee "up" (free the spot on first layer)
            else:
                beeGrid_2nd[self.i,self.j]=FREE
            
            self.move_toward_dir(beeGrid_2nd,init_pos)
            
            # update beeGrid_2nd with the new position (and if bee is static or moved)
            if self.i==init_pos[0] and self.j==init_pos[1]:
                beeGrid_2nd[self.i,self.j]=STAT
            else:
                beeGrid_2nd[self.i,self.j]=MOV

        elif self.state=='explore':
            beeGrid_2nd[self.i,self.j]=FREE
            
            # if hit a wall, draw a new direction on another wall
            if self.i == self.imax:
                self.draw_direction(bounced=True,exclude='down')
            if self.i == 0:
                self.draw_direction(bounced=True,exclude='up')
            if self.j == self.jmax:
                self.draw_direction(bounced=True,exclude='right')
            if self.j == 0:
                self.draw_direction(bounced=True,exclude='left')

            self.move_toward_dir(beeGrid_2nd,init_pos)

            # update beeGrid with the new position (and if bee is static or moved)
            if self.i==init_pos[0] and self.j==init_pos[1]:
                beeGrid_2nd[self.i,self.j]=STAT
            else:
                beeGrid_2nd[self.i,self.j]=MOV