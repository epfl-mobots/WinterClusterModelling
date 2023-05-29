import numpy as np
import matplotlib.pyplot as plt
import glob
import cv2


path = "C:/Users/Louise/Documents/EPFL/MA4/Project/data/annotations/surf/"
files = glob.glob(path+'2201*.png')
print(len(path))
BLUE = [255,0,0]
RED = [0,0,255]

c1 = BLUE
c2 = RED

image = cv2.imread(files[0])
nb_c1 = np.count_nonzero(np.all(image==BLUE,axis=2))
nb_c2 = np.count_nonzero(np.all(image==RED,axis=2))
frac = nb_c2/nb_c1
res= [[files[0][0:64],nb_c1,nb_c2,frac]]

one_col = [0]
fifteen = []
print(res[-1])
for f in files[1:]:
    image = cv2.imread(f)
    nb_c1 = np.count_nonzero(np.all(image==c1,axis=2))
    nb_c2 = np.count_nonzero(np.all(image==c2,axis=2))

    frac = nb_c2/(nb_c1+nb_c2)
    res.append([f[65:],nb_c1,nb_c2,frac])
    print(res[-1])
    #print(f, " : blue = ", nb_blue, " red = ", nb_red)
#print(res)
