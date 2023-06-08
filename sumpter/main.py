from sim import Sim
import numpy as np
from tqdm import tqdm

'''#default parameters
bee_param = {
    "Tcoma" : 8,
    "TminI" : 18,
    "TmaxI" : 23,
    "xmax"  : 49,
    "ymax"  : 99
}

hotspot = {
    "coord" : [[0,3],[1,3]], #change
    "Tspot" : 20.5, #change
    "on" : 15 #change
}

hive_param = {
    "init_shape" : "random",
    "dims_b" : (50,100),
    "n_bees" : 200,
    "tau" : 8,
    "g" : 2,
    "bee_param" : bee_param,
    "dims_temp" : (100,200), 
    "tempA" : 13,  #change
    "lambda_air" : 1.0,
    "lambda_bee" : 0.45,
    "hq20" : 0.037,
    "gamma" : np.log(2.4)/10
}'''

EXPERIMENTS = True
SUMPTER = False

if EXPERIMENTS : #bunch of simulations
    c=0
    dr = [100,10,1000]

    alphas = [0.002,0]#[2,4]#3
    ambient_temperatures = [12]
    n_bees = [200]
    folds = 1

    for T_amb in ambient_temperatures:
        for a in alphas:
            for k in range(folds):
                bee_param = {
                    "Tcoma" : 8,
                    "TminI" : 18,
                    "TmaxI" : 23,
                    "xmax"  : 49,
                    "ymax"  : 99,
                    "prob_mode" : 'temp_dep',
                    "alpha" : a
                }

                hotspot = {
                    "j_c" : 4/5,
                    "i_c" : 1/2,
                    "sz" : 1/4,
                    "coord" : [],
                    "Tspot" : 20.5, #change
                    "on" : 0, #change
                    "off" : 100000
                }

                hive_param = {
                    "init_shape" : "disc",
                    "dims_b" : (50,100),
                    "n_bees" : 200,
                    "tau" : 8,
                    "g" : 2,
                    "bee_param" : bee_param,
                    "dims_temp" : (100,200), 
                    "tempA" : T_amb,  #change
                    "lambda_air" : 1.0,
                    "lambda_bee" : 0.45,
                    "hq20" : 0.037,
                    "gamma" : np.log(2.4)/10
                }

                if T_amb==13:
                    SIM_TIME = 10000 #in bee timesteps
                if T_amb<13:
                    SIM_TIME = 40000 #in bee timesteps

                sim = Sim(hive_param,draw_on=True,hotspot=hotspot,draw_t=dr[k]) #the simulation is redrawn every DRAW_T steps
                for i in tqdm(range(SIM_TIME)):
                    sim.update()
                    if i%10000==0:
                        sim.save()

                sim.end()
                print(c)
                c=c+1


if SUMPTER : #bunch of simulations
    c=0
    dr = [100,10,1000]

    alphas = [0.001]#[2,4]#3
    ambient_temperatures = [11,13,12,10]
    n_bees = [200]
    folds = 1

    for T_amb in ambient_temperatures:
        for a in alphas:
            for k in range(folds):
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
                    "Tspot" : 20.5, #change
                    "on" : 10000, #change
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
                    "tempA" : T_amb,  #change
                    "lambda_air" : 1.0,
                    "lambda_bee" : 0.45,
                    "hq20" : 0.037,
                    "gamma" : np.log(2.4)/10
                }

                if T_amb>=11:
                    SIM_TIME = 20000 #in bee timesteps
                if T_amb<13:
                    SIM_TIME = 20000 #in bee timesteps

                sim = Sim(hive_param,draw_on=True,hotspot=hotspot,draw_t=dr[k]) #the simulation is redrawn every DRAW_T steps
                for i in tqdm(range(SIM_TIME)):
                    sim.update()
                    if i%10000==0:
                        sim.save()

                sim.end()
                print(c)
                c=c+1


else: #only one simulation
    # hotspot = {
    #     "coord" : [[0,4],[1,4]], #change
    #     "Tspot" : 20.5, #change
    #     "on" : 200, #change
    #     "off" : 5000
    # }

    bee_param = {
        "Tcoma" : 8,
        "TminI" : 18,
        "TmaxI" : 23,
        "xmax"  : 49,
        "ymax"  : 99,
        "prob_mode" : 'temp_dep',
        "alpha" : 0.001
    }

    hotspot = {
        "j_c" : 4/5,
        "i_c" : 1/2,
        "sz" : 1/4,
        "coord" : [],
        "Tspot" : 20.5, #change
        "on" : 0, #change
        "off" : 100000
    }

    hive_param = {
        "init_shape" : "disc",
        "dims_b" : (50,100),
        "n_bees" : 200,
        "tau" : 8,
        "g" : 2,
        "bee_param" : bee_param,
        "dims_temp" : (100,200), 
        "tempA" : 9,  #change
        "lambda_air" : 1.0,
        "lambda_bee" : 0.45,
        "hq20" : 0.037,
        "gamma" : np.log(2.4)/10
    }

    SIM_TIME = 20000 #in bee timesteps

    sim = Sim(hive_param,draw_on=True,hotspot=hotspot,draw_t=10) #the simulation is redrawn every DRAW_T steps
    for i in tqdm(range(SIM_TIME)):
        sim.update()
        if i%1000==0:
            sim.save()
        #print(i)

    sim.end()