"""Selection of directories to plot data from"""

import numpy as np
import gc
import os
import glob
from configparser import ConfigParser

from plot_temp import plot_combined, plot_test

#Replace with desired path
data_path = "../data/"
dir_path = "10C/sumpter/2024-11-22T11_32_58/it_797/"

dir = data_path+dir_path

if not os.path.isdir(dir+"analysis"):
    os.mkdir(dir+"analysis")

# Fetch the config file from the directory above
cfg_path = glob.glob(dir+"../config*")[0]
# Open the associated config file
cfg = ConfigParser()
cfg.read(cfg_path)
#plot_combined(dir,cfg)
plot_test(dir,cfg)
    