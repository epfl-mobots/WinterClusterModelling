from matplotlib.colors import LinearSegmentedColormap, hsv_to_rgb
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import gc

T_MIN_DRAW = 9
T_MAX_DRAW = 27
SIZE_BEE = 1

colors=[]
for i in range(5):
    col = hsv_to_rgb((2/3-i*1/6,1,1))
    col = np.append(col,1.)
    colors.append(col)
cmap_temp = LinearSegmentedColormap.from_list("mycmap", colors)

def update(hive,path,count=0):
    #plotting temperatures as background
    #temp_colors = (-1/(T_MAX_DRAW-T_MIN_DRAW))*hive.tempField+(T_MAX_DRAW/(T_MAX_DRAW-T_MIN_DRAW))*np.ones_like(hive.tempField)
    #plt.matshow(hive.tempField,fignum=count,cmap=cmap_temp,vmin=0,vmax=0.9,aspect='equal',interpolation='none',origin='lower')
    plt.matshow(hive.tempField,fignum=count,cmap=cmap_temp,aspect='equal',interpolation='none',origin='lower',norm=matplotlib.colors.Normalize(vmin=T_MIN_DRAW,vmax=T_MAX_DRAW))

    #color bar
    #vals = 0.1*np.array(range(0,10))
    plt.colorbar(location='top',shrink=0.8,spacing='proportional',ticks=range(int(np.min(hive.tempField)),int(np.max(hive.tempField)+2)))
    #cbar.ax.set_xticklabels((-1/(T_MAX_DRAW-T_MIN_DRAW))*vals+(T_MAX_DRAW/(T_MAX_DRAW-T_MIN_DRAW))*np.ones_like(vals))


    #plotting bees
    for b in hive.colony:
        plt.scatter(b.j*hive.g,b.i*hive.g,c='black',s=SIZE_BEE)

    #print centroid position and temperature (bottom right)
    plt.scatter(hive.centroid[1]*hive.g,hive.centroid[0]*hive.g,c='red',s=2)
    # T = str(hive.Tc[-1])
    # plt.text(75,5,"Tc: "+T[0:6]+"C",c='red')

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

