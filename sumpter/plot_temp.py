import matplotlib.pyplot as plt
import matplotlib
import pickle
import numpy as np

def xU(grid):
    exp = np.sum(grid[0])/49
    xU = np.zeros((1,len(grid)))
    for i in range(len(grid)):
        n_y = np.sum(grid[i],axis=1)
        xU[i]=np.sum((1/exp)*np.square(n_y-exp))
    print(xU)
    return xU

path = "C:/Users/Louise/Documents/EPFL/MA4/Project/data/"

# dir = ["2023-04-03T12_25_31/"]
# plt.figure()
# for d in dir:
#     f = open(path+d+"beeGrid.obj", "rb")
#     bg = pickle.load(f)
#     f.close()
#     print(len(bg))
#     x = xU(bg)
#     plt.plot(range(len(x)),x)
#     plt.show()




# dir = ["2023-04-03T15_36_48/","2023-04-03T15_52_29/","2023-04-03T16_04_40/","2023-04-03T16_17_13/","2023-04-03T16_35_44/"]
# #evolution of Tmax over simulation time
# for d in dir:
#     f = open(path+d+"Tmax.obj", "rb")
#     Tmax = pickle.load(f)
#     f.close()
#     plt.plot(range(len(Tmax)),Tmax)
# plt.show()

#bee distribution over time (along the x axis)
d = "old_colors/2023-04-03T16_35_44/"
f = open(path+d+"beeGrid.obj", "rb")
beegrid = pickle.load(f)
f.close()

beedistri = np.sum(beegrid,axis=0)
print(np.shape(np.array(beegrid)))
print(len(beedistri))

for i in np.linspace(0,len(beedistri),10,dtype=int):
    plt.figure()
    plt.plot(range(len(beedistri[:,i])),beedistri[:,i])
    plt.show()

