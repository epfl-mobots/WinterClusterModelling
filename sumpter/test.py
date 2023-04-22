from matplotlib.colors import LinearSegmentedColormap, hsv_to_rgb
import numpy as np
import matplotlib.pyplot as plt


a = np.array([[0,3,4,5,5],[1,3,6,7,8],[0,3,4,5,5]])
print(a[0:2,2:5])

colors=[]
for i in range(5):
    col = hsv_to_rgb((0+i*1/6,1,1))
    col = np.append(col,1.)
    colors.append(col)
cmap1 = LinearSegmentedColormap.from_list("mycmap", colors)

r = 1/10000*np.array(range(10000))
mat = np.reshape(r,(100,100))
print(mat)
plt.matshow(mat, cmap=cmap1,aspect='equal',interpolation='none',origin='lower')
plt.show()