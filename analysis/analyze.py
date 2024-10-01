"""Selection of directories to plot data from"""

import numpy as np
import gc
import os
import glob
from configparser import ConfigParser

from plot_temp import plot_temperature, plot_combined, plot_bee_distrib, plot_combined_hive

#Replace with desired path
data_path = "../data/"
dir_path = "12.0C/sumpter/2024-09-30T12_36_00/it_106/"

dir = data_path+dir_path

if not os.path.isdir(dir+"analysis"):
    os.mkdir(dir+"analysis")

# Fetch the config file from the directory above
cfg_path = glob.glob(dir+"../config*")[0]
# Open the associated config file
cfg = ConfigParser()
cfg.read(cfg_path)
plot_combined(dir,cfg)
    