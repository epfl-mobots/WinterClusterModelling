import matplotlib.pyplot as plt
import matplotlib
import pickle
import numpy as np
import gc
import os
import glob
from tqdm import tqdm

def xU(grid):
    exp = np.sum(grid[0])/49
    xU = np.zeros((1,len(grid)))
    for i in range(len(grid)):
        n_y = np.sum(grid[i],axis=1)
        xU[i]=np.sum((1/exp)*np.square(n_y-exp))
    print(xU)
    return xU

