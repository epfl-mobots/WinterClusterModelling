"""Selection of directories to plot data from"""

import numpy as np
import gc
import os
import glob

from plot_temp import plot_temperature, plot_combined, plot_bee_distrib, plot_combined_hive

#Replace with desired path
path = "../data/"

#dir = glob.glob(path+'2023-0*')
dir = [path+"12C/sump/2023-07-04T15_46_13/it_10001/"]

for d in dir:
    if not os.path.isdir(d+"analysis"):
        os.mkdir(d+"analysis")

    plot_combined(d)
    