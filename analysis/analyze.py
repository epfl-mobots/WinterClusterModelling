import numpy as np
import gc
import os
import glob

from plot_temp import plot_temperature, plot_combined, plot_bee_distrib,plot_combined_hive
from stats import *

path = "C:/Users/Louise/Documents/EPFL/MA4/Project/data/"

#dir = glob.glob(path+'2023-0*')
dir = [path+"9C/sump/2023-05-25T15_30_13/it_10000/"]

for d in dir:
    if not os.path.isdir(d+"analysis"):
        os.mkdir(d+"analysis")

    plot_combined(d)
    