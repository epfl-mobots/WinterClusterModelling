import matplotlib.pyplot as plt
import matplotlib
import pickle
import numpy as np
import gc
import os
import glob

# def xU(grid):
#     exp = np.sum(grid[0])/49
#     xU = np.zeros((1,len(grid)))
#     for i in range(len(grid)):
#         n_y = np.sum(grid[i],axis=1)
#         xU[i]=np.sum((1/exp)*np.square(n_y-exp))
#     print(xU)
#     return xU

path = "C:/Users/Louise/Documents/EPFL/MA4/Project/data/"

dir = glob.glob(path+'2023-04-2*/')
plt.figure()
for d in dir:
    if not os.path.isdir(d+"analysis"):
        os.mkdir(d+"analysis")
    # get beegrid of the simulation
    f = open(d+"beeGrid.obj", "rb")
    bg = pickle.load(f)
    f.close()
    bg = np.array(bg[1:])

    # get temperature field
    f = open(d+"T_field.obj", "rb")
    temp_field = np.array(pickle.load(f))
    f.close()
    print(len(temp_field), len(temp_field[0]),len(temp_field[0][0]))

    # for i in range(99):
    #     centroid = np.mean(np.argwhere(bg[i]),axis=0)
    #     print(centroid)
    #     plt.scatter(i,centroid[0])
    # plt.show()

    if not os.path.isdir(d+"analysis/bee"):
        os.mkdir(d+"analysis/bee")
        os.mkdir(d+"analysis/temp")
        os.mkdir(d+"analysis/combined")

    times = range(0,len(temp_field)-1,10)
    for t in times:
        per_col = np.sum((bg[t]!=0),axis=0)
        plt.bar(range(len(per_col)),per_col)
        plt.ylim((0,100))
        #plt.show()
        plt.savefig(d+"analysis/bee/it_{}.png".format(t))

        centroid = np.mean(np.argwhere(bg[t]),axis=0)
        plt.plot(range(200),temp_field[t,int(centroid[0]),:])
        plt.ylim((9,25))
        #plt.show()
        plt.savefig(d+"analysis/temp/it_{}.png".format(t))


        fig, ax1 = plt.subplots() 
        ax1.set_ylabel('n_bees', color = 'red') 
        ax1.set_ylim((0,100))
        ax1.bar(range(0,200,2), 2*per_col, color = 'red')         
        # Adding Twin Axes
        ax2 = ax1.twinx() 
        ax2.set_ylabel('temperature', color = 'blue') 
        ax2.set_ylim((9,25))
        ax2.plot(range(200), temp_field[t,int(centroid[0]),:], color = 'blue') 
        plt.savefig(d+"analysis/combined/it_{}.png".format(t))

        # Close figure, clear everything
        plt.cla() 
        plt.clf() 
        plt.close('all')   
        gc.collect()




# dir = ["2023-04-03T15_36_48/","2023-04-03T15_52_29/","2023-04-03T16_04_40/","2023-04-03T16_17_13/","2023-04-03T16_35_44/"]
# #evolution of Tmax over simulation time
# for d in dir:
#     f = open(path+d+"Tmax.obj", "rb")
#     Tmax = pickle.load(f)
#     f.close()
#     plt.plot(range(len(Tmax)),Tmax)
# plt.show()

#bee distribution over time (along the x axis)
# d = "old_colors/2023-04-03T16_35_44/"
# f = open(path+d+"beeGrid.obj", "rb")
# beegrid = pickle.load(f)
# f.close()

# beedistri = np.sum(beegrid,axis=0)
# print(np.shape(np.array(beegrid)))
# print(len(beedistri))

# for i in np.linspace(0,len(beedistri),10,dtype=int):
#     plt.figure()
#     plt.plot(range(len(beedistri[:,i])),beedistri[:,i])
#     plt.show()

