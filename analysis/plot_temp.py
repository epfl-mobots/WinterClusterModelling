"""Definition of plotting functions to analyze the data generated during a simulation
- plot_temperature
- plot_bee_distrib
- plot_combined
- plot_combined_hive
"""

import matplotlib.pyplot as plt
import matplotlib
import pickle
import numpy as np
import gc
import os
import glob
from tqdm import tqdm
import sys
sys.path.append("../src")
from frame import Frame
from bee import Bee

def plot_temperature(srcDir):
    """ Plots centroid and max temperature across rows from data in srcDir. 
    One plot is created for each timestep of the simulation and saved in the "analysis" subfolder.
    ONLY WORKS FOR OLD WAY OF SAVING DATA
    """
    if not os.path.isdir(srcDir+"/analysis"):
        os.mkdir(srcDir+"/analysis")

    # get beegrid of the simulation
    f = open(srcDir+"/beeGrid.obj", "rb")
    bg = pickle.load(f)
    f.close()

    # get temperature field
    f = open(srcDir+"/T_field.obj", "rb")
    temp_field = np.array(pickle.load(f))
    f.close()

    if not os.path.isdir(srcDir+"/analysis/temp"):
        os.mkdir(srcDir+"/analysis/temp")
    outDir = srcDir+"/analysis/temp"
    
    times = range(0,len(temp_field)-1,10)
    
    for t in tqdm(times):
        centroid = np.mean(np.argwhere(bg[t]),axis=0)
        plt.plot(range(200),temp_field[t,int(centroid[0]),:])
        plt.ylim((9,25))
        plt.savefig(outDir+"/it_{}.png".format(t))

        #close figure, clear everything
        plt.cla() 
        plt.clf() 
        plt.close('all')   
        gc.collect()


def plot_bee_distrib(srcDir):
    """ Plots bee distribution by column from data in srcDir. 
    One plot is created for each timestep of the simulation and saved in the "analysis" subfolder.
    ONLY WORKS FOR OLD WAY OF SAVING DATA
    """
    if not os.path.isdir(srcDir+"/analysis"):
        os.mkdir(srcDir+"/analysis")

    # get beegrid of the simulation
    f = open(srcDir+"/beeGrid.obj", "rb")
    bg = pickle.load(f)
    f.close()

    f = open(srcDir+"/beeGrid_2nd.obj", "rb")
    bg_2 = pickle.load(f)
    f.close()
    bg = np.array(bg[1:])

    if not os.path.isdir(srcDir+"/analysis/bee"):
        os.mkdir(srcDir+"/analysis/bee")
    outDir = srcDir+"/analysis/bee"
    
    times = range(0,len(bg)-1,10)
    
    for t in tqdm(times):
        #plot with bee bars for columns
        per_col = np.sum((bg[t]!=0),axis=0)
        per_col = per_col+np.sum((bg_2[t]!=0),axis=0)
        plt.bar(range(len(per_col)),per_col)
        plt.ylim((0,100))
        plt.savefig(outDir+"/bee/it_{}.png".format(t))

        #close figure, clear everything
        plt.cla() 
        plt.clf() 
        plt.close('all')   
        gc.collect()


def plot_combined_old(srcDir):
    """ Plots bee distribution by column along with centroid and max temperature from data in srcDir. 
    One plot is created for each timestep of the simulation and saved in the "analysis" subfolder.
    ONLY WORKS FOR OLD WAY OF SAVING DATA
    """
    if not os.path.isdir(srcDir+"/analysis"):
        os.mkdir(srcDir+"/analysis")

    # get beegrid of the simulation
    f = open(srcDir+"/beeGrid.obj", "rb")
    bg = pickle.load(f)
    f.close()

    f = open(srcDir+"/beeGrid_2nd.obj", "rb")
    bg_2 = pickle.load(f)
    f.close()
    bg = np.array(bg[1:])

    # get temperature field
    f = open(srcDir+"/T_field.obj", "rb")
    temp_field = np.array(pickle.load(f))
    f.close()

    if not os.path.isdir(srcDir+"/analysis/combined"):
        os.mkdir(srcDir+"/analysis/combined")
    outDir = srcDir+"/analysis/combined"
    
    times = range(0,len(temp_field)-1,10)
    
    for t in tqdm(times):
        #computing bee positions
        per_col = np.sum((bg[t]!=0),axis=0)
        per_col = per_col+np.sum((bg_2[t]!=0),axis=0)
        centroid = np.mean(np.argwhere(bg[t]),axis=0)

        fig, ax1 = plt.subplots() 
        ax1.set_ylabel('Number of agents', color = 'red') 
        ax1.set_ylim((0,100))
        ax1.set_xlabel('Column')
                
        # Adding Twin Axes
        temp_to_plot = temp_field[t,int(centroid[0]),:]
        min_temps = temp_field[t,:,:].min(axis=0)
        max_temps = temp_field[t,:,:].max(axis=0)

        # computing area to shade
        idxs_up = max_temps>18
        idxs_down = max_temps<23
        idxs_comf = np.nonzero(idxs_up & idxs_down)[0]

        #plotting curve of temperature across i of bee centroid position
        ax2 = ax1.twinx() 
        ax2.set_ylabel('Temperature [°C]', color = 'blue') 
        
        ax2.set_ylim((9,25))
        ax2.plot(range(200), temp_to_plot, color = 'blue')
        ax2.plot(range(200), min_temps, color = 'blue', linestyle='--', linewidth=0.5)
        ax2.plot(range(200), max_temps, color = 'blue', linestyle='--', linewidth=0.5)
        #shading comfort area
        #ax2.fill_between(idxs_comf,max_temps[idxs_comf],alpha=0.3)

        ax1.bar(range(0,200,2), 2*per_col, color = 'red') 
        plt.savefig(outDir+"/it_{}.png".format(t))

        # Close figure, clear everything
        plt.cla() 
        plt.clf() 
        plt.close('all')   
        gc.collect()

def plot_combined_hive(srcDir):
    """ Plots bee distribution by column along with centroid and max temperature from data in srcDir. 
    Plots are saved in the "analysis" subfolder.
    # ONLY WORKS FOR OLD WAY OF SAVING DATA (until 12th January 2023)
    """
    if not os.path.isdir(srcDir+"/analysis"):
        os.mkdir(srcDir+"/analysis")

    # get beegrid of the simulation
    f = open(srcDir+"/frame.obj", "rb")
    frame_save = pickle.load(f)
    f.close()

    bg = frame_save.bgs_save 
    bg_2 = frame_save.bgs2_save
    bg = np.array(bg[1:])
    temp_field = np.array(frame_save.tempField_save)
    

    if not os.path.isdir(srcDir+"/analysis/combined"):
        os.mkdir(srcDir+"/analysis/combined")
    outDir = srcDir+"/analysis/combined"
    
    times = range(0,len(temp_field)-1,25)
    
    for t in tqdm(times):
        #computing bee positions
        per_col = np.sum((bg[t]!=0),axis=0)
        per_col = per_col+np.sum((bg_2[t]!=0),axis=0)
        centroid = np.mean(np.argwhere(bg[t]),axis=0)

        fig, ax1 = plt.subplots() 
        ax1.set_ylabel('Number of agents', color = 'red') 
        ax1.set_ylim((0,100))
        ax1.set_xlabel('Column')
                
        # Adding Twin Axes
        temp_to_plot = temp_field[t,frame_save.g*int(centroid[0]),:]
        min_temps = temp_field[t,:,:].min(axis=0)
        max_temps = temp_field[t,:,:].max(axis=0)

        #plotting curve of temperature across i of bee centroid position
        ax2 = ax1.twinx() 
        ax2.set_ylabel('Temperature [°C]', color = 'blue') 
        ax2.set_ylim((10,35))
        ax2.plot(range(200), temp_to_plot, color = 'blue')
        ax2.plot(range(200), min_temps, color = 'blue', linestyle='--', linewidth=0.5)
        ax2.plot(range(200), max_temps, color = 'blue', linestyle='--', linewidth=0.5)
        #shading comfort area
        #ax2.fill_between(idxs_comf,max_temps[idxs_comf],alpha=0.3)

        # Extract Tmin and Tmax of comfort zone from bees' config file
        Tmin = frame_save.colony[0].TminI
        Tmax = frame_save.colony[0].TmaxI

        ax2.fill_between(range(200), temp_to_plot, where=((temp_to_plot >= Tmin) & (temp_to_plot <= Tmax)), color='blue', alpha=0.3, label='Comfort zone for bees')


        ax1.bar(range(0,200,2), 2*per_col, color = 'red') 
        plt.savefig(outDir+"/it_{}.png".format(t))

        # Close figure, clear everything
        plt.cla() 
        plt.clf() 
        plt.close('all')   
        gc.collect()


def plot_combined(srcDir, cfg):
    """ Plots bee distribution by column along with centroid and max temperature from data in srcDir. 
    Plots are saved in the "analysis" subfolder.
    param srcDir: path to the directory containing the data (containging frame.obj)
    param cfg: ConfigParser object containing the configuration of the simulation
    """
    if not os.path.isdir(srcDir+"/analysis"):
        os.mkdir(srcDir+"/analysis")

    # get beegrid of the simulation
    f = open(srcDir+"/frame.obj", "rb")
    frame_save = pickle.load(f)
    f.close()

    bg = frame_save.bgs_save 
    bg_2 = frame_save.bgs2_save
    print(np.sum(bg[0]))
    #bg = np.array(bg[1:]) # Not sure why this was done
    temp_field = np.array(frame_save.tempField_save)
    

    if not os.path.isdir(srcDir+"/analysis/combined"):
        os.mkdir(srcDir+"/analysis/combined")
    outDir = srcDir+"/analysis/combined"
    
    iterations = range(0,len(temp_field)-1,25)
    
    for iteration in tqdm(iterations):
        #computing bee positions
        per_col = np.sum((bg[iteration]!=0),axis=0)
        per_col = per_col+np.sum((bg_2[iteration]!=0),axis=0)
        centroid = np.mean(np.argwhere(bg[iteration]),axis=0)

        fig, ax1 = plt.subplots() 
        ax1.set_ylabel('Number of agents', color = 'red') 
        ax1.set_ylim((0,100))
        ax1.set_xlabel('Column')
                
        # Adding Twin Axes
        temp_to_plot = temp_field[iteration,frame_save.g*int(centroid[0]),:]
        min_temps = temp_field[iteration,:,:].min(axis=0)
        max_temps = temp_field[iteration,:,:].max(axis=0)

        #plotting curve of temperature across i of bee centroid position
        ax2 = ax1.twinx() 
        ax2.set_ylabel('Temperature [°C]', color = 'blue') 
        ax2.set_ylim((10,35))
        ax2.plot(range(200), temp_to_plot, color = 'blue')
        ax2.plot(range(200), min_temps, color = 'blue', linestyle='--', linewidth=0.5)
        ax2.plot(range(200), max_temps, color = 'blue', linestyle='--', linewidth=0.5)

        # Extract Tmin and Tmax of comfort zone from bees' config file
        # Tmin = frame_save.colony[0].TminI
        # Tmax = frame_save.colony[0].TmaxI
        Tmin = cfg.getfloat('bee','TminI')
        Tmax = cfg.getfloat('bee','TmaxI')
        
        #shading comfort area
        ax2.fill_between(range(200), temp_to_plot, where=((temp_to_plot >= Tmin) & (temp_to_plot <= Tmax)), color='blue', alpha=0.3, label='Comfort zone for bees')


        ax1.bar(range(0,200,2), 2*per_col, color = 'red') 
        plt.savefig(outDir+"/it_{}.png".format(iteration))

        # Close figure, clear everything
        plt.cla() 
        plt.clf() 
        plt.close('all')   
        gc.collect()
