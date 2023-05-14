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

if EXPERIMENTS : #bunch of simulations
    c=0
    dr = [1,100,1000]

    alphas = [0.001]#[2,4]#3
    ambient_temperatures = [9,13]
    folds = 3

    for a in alphas:
        for T_amb in ambient_temperatures:
            for k in range(folds):
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
                    "coord" : [[0,4],[1,4]], #change
                    "Tspot" : 20.5, #change
                    "on" : 200 #change
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
                    SIM_TIME = 4000 #in bee timesteps
                if T_amb==9:
                    SIM_TIME = 5000 #in bee timesteps

                sim = Sim(hive_param,draw_on=True,hotspot=hotspot,draw_t=dr[k]) #the simulation is redrawn every DRAW_T steps
                for i in tqdm(range(SIM_TIME)):
                    sim.update()
                    if i%1000==0:
                        sim.save()

                sim.end()
                print(c)
                c=c+1


else: #only one simulation
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
        "coord" : [[0,4],[1,4]], #change
        "Tspot" : 20.5, #change
        "on" : 200, #change
        "off" : 5000
    }

    hive_param = {
        "init_shape" : "disc",
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
    }
    SIM_TIME = 4000 #in bee timesteps

    sim = Sim(hive_param,draw_on=True,hotspot=hotspot,draw_t=1) #the simulation is redrawn every DRAW_T steps
    for i in tqdm(range(SIM_TIME)):
        sim.update()
        if i%1000==0:
            sim.save()
        #print(i)

    sim.end()