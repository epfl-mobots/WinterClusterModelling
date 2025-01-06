"""Definition of drawing functions to generate graphic representation of simulation"""

from matplotlib.colors import LinearSegmentedColormap, hsv_to_rgb
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import gc

from bee import FREE

T_MIN_DRAW = 5
T_MAX_DRAW = 35
SIZE_BEE = 1

colors=[]
for i in range(5):
    col = hsv_to_rgb((2/3-i*1/6,1,1))
    col = np.append(col,1.)
    colors.append(col)
cmap_temp = LinearSegmentedColormap.from_list("mycmap", colors)

def update(frame,path,count=None):
    """Draw the simulation state described by frame and save image in path"""
    #plotting temperatures as background
    #plt.matshow(frame.tempField,cmap='viridis',aspect='equal',interpolation='none',origin='lower',norm=matplotlib.colors.Normalize(vmin=np.min(frame.tempField),vmax=np.max(frame.tempField)))
    plt.matshow(frame.tempField,cmap='viridis',aspect='equal',interpolation='none',origin='lower',norm=matplotlib.colors.Normalize(vmin=T_MIN_DRAW,vmax=T_MAX_DRAW))
    
    #color bar
    ticks = np.arange(T_MIN_DRAW, T_MAX_DRAW+1, 5)
    plt.colorbar(location='top',shrink=0.8,spacing='proportional',ticks=ticks, label=f'Temperature [°C]         (Max={np.round(np.max(frame.tempField))}°C)')
    
    #plotting bees
    for b in frame.colony:
        if b.state=='sumpter' :
            if frame.beeGrid_2nd[b.i,b.j]!=FREE: #if there is a bee in the 2nd layer
                plt.scatter(b.j*frame.g,b.i*frame.g,c='red',s=1.5*SIZE_BEE, zorder=4)
            else:
                if b.thermogenesis == True:
                    plt.scatter(b.j*frame.g,b.i*frame.g,c='red',s=2*SIZE_BEE, zorder=4)   
                plt.scatter(b.j*frame.g,b.i*frame.g,c='orange',s=SIZE_BEE, zorder=3)
        elif b.state=='leave':
            if frame.beeGrid[b.i,b.j]!=FREE: #if there is a bee in the first layer
                plt.scatter(b.j*frame.g,b.i*frame.g,c='red',s=1.5*SIZE_BEE, zorder=3)
            else:
                plt.scatter(b.j*frame.g,b.i*frame.g,c='red',s=SIZE_BEE,marker='D', zorder=3)
        elif b.state=='explore':
            plt.scatter(b.j*frame.g,b.i*frame.g,c='green',s=SIZE_BEE, zorder=3)


    #Plotting frame
    if frame.RealisticFrame:
        plt.plot([frame.outside*frame.g - 0.5, frame.dims_temp[1] - frame.outside*frame.g - 0.5], [frame.outside*frame.g - 0.5, frame.outside*frame.g - 0.5], color='black')
        plt.plot([frame.outside*frame.g - 0.5, frame.dims_temp[1] - frame.outside*frame.g - 0.5], [(frame.outside + frame.single_height)*frame.g - 0.5, (frame.outside + frame.single_height)*frame.g - 0.5], color='black')
        plt.plot([frame.outside*frame.g - 0.5, frame.dims_temp[1] - frame.outside*frame.g - 0.5], [(frame.outside + frame.single_height - frame.t)*frame.g - 0.5, (frame.outside + frame.single_height - frame.t)*frame.g - 0.5], color='black')
        plt.plot([frame.outside*frame.g - 0.5, frame.dims_temp[1] - frame.outside*frame.g - 0.5], [(frame.outside + frame.single_height + frame.b)*frame.g - 0.5, (frame.outside + frame.single_height + frame.b)*frame.g -0.5], color='black')
        plt.plot([frame.outside*frame.g - 0.5, frame.dims_temp[1] - frame.outside*frame.g - 0.5], [frame.dims_temp[0] -(frame.outside + frame.t)*frame.g - 0.5, frame.dims_temp[0] -(frame.outside + frame.t)*frame.g - 0.5], color='black')
        plt.plot([frame.outside*frame.g - 0.5, frame.dims_temp[1] - frame.outside*frame.g - 0.5], [frame.dims_temp[0] - frame.outside*frame.g - 0.5, frame.dims_temp[0] - frame.outside*frame.g - 0.5], color='black')
    
        plt.plot([frame.outside*frame.g - 0.5, frame.outside*frame.g- 0.5], [frame.outside*frame.g - 0.5, (frame.outside + frame.single_height)*frame.g - 0.5], color='black')
        plt.plot([frame.outside*frame.g - 0.5, frame.outside*frame.g- 0.5], [(frame.outside + frame.single_height + frame.b)*frame.g - 0.5, frame.dims_temp[0] - frame.outside*frame.g - 0.5], color='black')
        plt.plot([frame.dims_temp[1] - frame.outside*frame.g - 0.5, frame.dims_temp[1] - frame.outside*frame.g- 0.5], [frame.outside*frame.g - 0.5, (frame.outside + frame.single_height)*frame.g - 0.5], color='black')
        plt.plot([frame.dims_temp[1] - frame.outside*frame.g - 0.5, frame.dims_temp[1] - frame.outside*frame.g- 0.5], [(frame.outside + frame.single_height + frame.b)*frame.g - 0.5, frame.dims_temp[0] - frame.outside*frame.g - 0.5], color='black')
    
    
    #remove axes ticks
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False,labeltop=False)
    plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
    if count is not None:
        plt.savefig(path+'iteration_{}.png'.format(count),  bbox_inches='tight')
    else:
        plt.savefig(path+'iteration_{}.png'.format(0),  bbox_inches='tight')
    #Close figure, clear everything
    plt.cla() 
    plt.clf() 
    plt.close('all')   
    plt.close(count)
    gc.collect()

