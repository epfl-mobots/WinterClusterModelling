"""Script to initiate simulations and set the parameters."""
from sim import Sim
import numpy as np
from tqdm import tqdm

#Parameter description with default values
# bee_param = {
#     "Tcoma" : 8,
#     "TminI" : 18,
#     "TmaxI" : 23,
#     "xmax"  : 49, #dimensions of the agents' possible positions
#     "ymax"  : 99,
#     "prob_mode" : 'temp_dep',
#     "alpha" : a
# }

# hotspot = {
#     "j_c" : 4/5, #if coord is an empty list, j position of hotspot as a fraction of the horizontal terrain dimension
#     "i_c" : 1/2, #if coord is an empty list, i position of hotspot as a fraction of the vertical terrain dimension
#     "sz" : 1/4, #if coord is an empty list, dimension of hotspot as a fraction of the vertical terrain dimension
#     "coord" : [[0,3]], #coordinates of the hotspot (first coordinate in [0,1], second in [0,4])
#     "Tspot" : 20.5, 
#     "on" : 0, #time at which the hotspot is turned on
#     "off" : 100000 #time at which the hotspot is turned off
# }

# hive_param = {
#     "init_shape" : "random", #can also be "disc" or "ring"
#     "dims_b" : (50,100), # Dimensions of the frame
#     "n_bees" : 200,
#     "tau" : 8, # bee time step
#     "g" : 2, # grid multiplication between temperature and bees
#     "bee_param" : bee_param,
#     "dims_temp" : (100,200), 
#     "tempA" : 13, 
#     "lambda_air" : 1.0,
#     "lambda_bee" : 0.45,
#     "hq20" : 0.037,
#     "gamma" : np.log(2.4)/10
# }

EXPERIMENTS = True
SUMPTER = False

if EXPERIMENTS: #bunch of simulations
    iteration=1
    dr = [1000]
    alphas = [0.002]
    ambient_temperatures = [12]
    ns_bees = [200]

    for T_amb in ambient_temperatures:
        for alpha in alphas:
            for refresh_rate in dr:
                for n_bees in ns_bees:
                    bee_param = {
                        "Tcoma" : 8,
                        "TminI" : 18,
                        "TmaxI" : 23,
                        "xmax"  : 49,
                        "ymax"  : 99,
                        "prob_mode" : 'temp_dep',
                        "alpha" : alpha
                    }

                    hotspot = {
                        "j_c" : 4/5,
                        "i_c" : 1/2,
                        "sz" : 1/4,
                        "coord" : [],
                        "Tspot" : 20.5, 
                        "on" : 0, 
                        "off" : 100000
                    }

                    hive_param = {
                        "init_shape" : "disc",
                        "dims_b" : (50,100),
                        "n_bees" : n_bees,
                        "tau" : 8,
                        "g" : 2,
                        "bee_param" : bee_param,
                        "dims_temp" : (100,200), 
                        "tempA" : T_amb,  
                        "lambda_air" : 1.0,
                        "lambda_bee" : 0.45,
                        "hq20" : 0.037,
                        "gamma" : np.log(2.4)/10
                    }

                    if T_amb==13:
                        SIM_TIME = 10000 #in bee timesteps
                    if T_amb<13:
                        SIM_TIME = 40000 #in bee timesteps

                    sim = Sim(hive_param,draw_on=True,hotspot=hotspot,draw_t=refresh_rate) #the simulation is redrawn every DRAW_T steps
                    for i in tqdm(range(SIM_TIME)):
                        sim.update()
                        if i%10000==0:
                            sim.save()

                    sim.end()
                    print(f"Simulation {iteration}/{len(alphas)*len(dr)*len(ambient_temperatures)*len(ns_bees)} finished.")
                    iteration=iteration+1


if SUMPTER : #bunch of simulations
    iteration=1
    dr = [1000]
    ns_bees = [200]
    alphas = [0.001]
    ambient_temperatures = [11,13,12,10]

    for T_amb in ambient_temperatures:
        for alpha in alphas:
            for refresh_rate in dr:
                for n_bees in ns_bees:
                    bee_param = {
                        "Tcoma" : 8,
                        "TminI" : 18,
                        "TmaxI" : 23,
                        "xmax"  : 49,
                        "ymax"  : 99,
                        "prob_mode" : 'temp_dep',
                        "alpha" : 0
                    }

                    hotspot = {
                        "j_c" : 4/5,
                        "i_c" : 1/2,
                        "sz" : 1/4,
                        "coord" : [],
                        "Tspot" : 20.5, 
                        "on" : 10000, 
                        "off" : 100000
                    }

                    hive_param = {
                        "init_shape" : "random",
                        "dims_b" : (50,100),
                        "n_bees" : 200,
                        "tau" : 8,
                        "g" : 2,
                        "bee_param" : bee_param,
                        "dims_temp" : (100,200), 
                        "tempA" : T_amb, 
                        "lambda_air" : 1.0,
                        "lambda_bee" : 0.45,
                        "hq20" : 0.037,
                        "gamma" : np.log(2.4)/10
                    }

                    if T_amb>=11:
                        SIM_TIME = 20000 #in bee timesteps
                    if T_amb<13:
                        SIM_TIME = 20000 #in bee timesteps

                    sim = Sim(hive_param,draw_on=True,hotspot=hotspot,draw_t=refresh_rate) #the simulation is redrawn every DRAW_T steps
                    for i in tqdm(range(SIM_TIME)):
                        sim.update()
                        if i%10000==0:
                            sim.save()

                    sim.end()
                    print(f"Simulation {iteration}/{len(alphas)*len(dr)*len(ambient_temperatures)*len(ns_bees)} finished.")
                    iteration=iteration+1
