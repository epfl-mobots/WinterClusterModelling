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

dir = ["2023-04-03T15_36_48/","2023-04-03T15_52_29/","2023-04-03T16_04_40/","2023-04-03T16_17_13/","2023-04-03T16_35_44/"]
for d in dir:
    f = open(path+d+"Tmax.obj", "rb")
    Tmax = pickle.load(f)
    f.close()
    plt.plot(range(len(Tmax)),Tmax)
plt.show()

x = np.arange(0, 100, 1)
x = np.arange(0, 100, 1)

# fig = plt.figure()
# ax = fig.gca()
# ax.set_xticks(np.arange(0, 100, 1))
# ax.set_yticks(np.arange(0, 100, 1))
# ax.set_aspect('equal')
# plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False,labeltop=False)
# plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
# #plt.scatter(x, y)
# plt.grid(b=True, which='major', color='black', linestyle='-')
# plt.grid(b=True, which='minor', color='grey', linestyle='-')
# plt.show()

matplotlib.ticker.AutoMinorLocator(2)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xticks(np.arange(0, 100, 1))
ax.set_yticks(np.arange(0, 100, 1))
ax.set_aspect('equal')
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False,labeltop=False)
plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
#ax.plot([1,2,3], [2,3,4], 'ro')
plt.minorticks_on()
for xmaj in ax.xaxis.get_majorticklocs():
  ax.axvline(x=xmaj, ls='-',c='grey',lw=0.5)
  ax.axvline(x=xmaj+0.5, ls='-',c='black',lw=0.5)

for ymaj in ax.yaxis.get_majorticklocs():
  ax.axhline(y=ymaj, ls='-',c='grey',lw=0.5)
  ax.axhline(y=ymaj+0.5, ls='-',c='black',lw=0.5)

plt.show()
