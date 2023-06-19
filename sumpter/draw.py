"""Definition of drawing functions to generate graphic representation of simulation"""

from matplotlib.colors import LinearSegmentedColormap, hsv_to_rgb
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import gc
from bee import FREE, STAT, MOV

T_MIN_DRAW = 5
T_MAX_DRAW = 25
SIZE_BEE = 1

colors=[]
for i in range(5):
    col = hsv_to_rgb((2/3-i*1/6,1,1))
    col = np.append(col,1.)
    colors.append(col)
cmap_temp = LinearSegmentedColormap.from_list("mycmap", colors)

def update(frame,path,count=0):
    """Draw the simulation state described by frame and save image in path"""
    #plotting temperatures as background
    plt.matshow(frame.tempField,fignum=count,cmap='viridis',aspect='equal',interpolation='none',origin='lower',norm=matplotlib.colors.Normalize(vmin=T_MIN_DRAW,vmax=T_MAX_DRAW))

    #color bar
    plt.colorbar(location='top',shrink=0.8,spacing='proportional',ticks=range(int(np.min(frame.tempField)),int(np.max(frame.tempField)+2)))

    #plotting bees
    for b in frame.colony:
        if b.state=='sumpter' :
            if frame.beeGrid_2nd[b.i,b.j]!=FREE: #if there is a bee in the 2nd layer
                plt.scatter(b.j*frame.g,b.i*frame.g,c='orange',s=1.5*SIZE_BEE)
            else:
                plt.scatter(b.j*frame.g,b.i*frame.g,c='black',s=SIZE_BEE)
        elif b.state=='leave':
            if frame.beeGrid[b.i,b.j]!=FREE: #if there is a bee in the first layer
                plt.scatter(b.j*frame.g,b.i*frame.g,c='orange',s=1.5*SIZE_BEE)
            else:
                plt.scatter(b.j*frame.g,b.i*frame.g,c='orange',s=SIZE_BEE,marker='D')
        elif b.state=='explore':
            plt.scatter(b.j*frame.g,b.i*frame.g,c='red',s=SIZE_BEE)

    #remove axes ticks
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False,labeltop=False)
    plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
    plt.savefig(path+'iteration_{}.png'.format(count))

    #Close figure, clear everything
    plt.cla() 
    plt.clf() 
    plt.close('all')   
    plt.close(count)
    gc.collect()

