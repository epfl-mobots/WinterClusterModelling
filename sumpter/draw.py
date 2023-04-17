from matplotlib.colors import LinearSegmentedColormap, hsv_to_rgb
import matplotlib.pyplot as plt
import numpy as np
import gc

T_MIN_DRAW = 10
T_MAX_DRAW = 30
SIZE_BEE = 1

colors=[]
for i in range(5):
    col = hsv_to_rgb((0+i*1/6,1,1))
    col = np.append(col,1.)
    colors.append(col)
cmap_temp = LinearSegmentedColormap.from_list("mycmap", colors)

def update(hive,path,count=0):
    #plotting temperatures as background
    temp_colors = (-1/(T_MAX_DRAW-T_MIN_DRAW))*hive.tempField+(T_MAX_DRAW/(T_MAX_DRAW-T_MIN_DRAW))*np.ones_like(hive.tempField)
    plt.matshow(temp_colors,fignum=count,cmap=cmap_temp,vmin=0,vmax=0.9,aspect='equal',interpolation='none',origin='lower')
    
    #plotting bees
    for b in hive.colony:
        plt.scatter(b.j*hive.g,b.i*hive.g,c='black',s=SIZE_BEE)

    #print centroid position and temperature (bottom right)
    plt.scatter(hive.centroid[1]*hive.g,hive.centroid[0]*hive.g,c='red',s=2)
    T = str(hive.Tc[-1])
    plt.text(75,5,"Tc: "+T[0:6]+"C",c='red')

    #remove axes ticks
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False,labeltop=False)
    plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
    #plt.show()
    plt.savefig(path+'iteration_{}.png'.format(count))

    # Close figure, clear everything
    plt.cla() 
    plt.clf() 
    plt.close('all')   
    plt.close(count)
    gc.collect()

