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

EXPERIMENTS = False

if EXPERIMENTS :
    dr = [10,1000,1000]

    hotspot_positions = [2,4]#3
    ambient_temperatures = [9,13,15]
    folds = 3

    for h in hotspot_positions:
        for T_amb in ambient_temperatures:
            for k in range(folds):
                bee_param = {
                    "Tcoma" : 8,
                    "TminI" : 18,
                    "TmaxI" : 23,
                    "xmax"  : 49,
                    "ymax"  : 99
                }

                hotspot = {
                    "coord" : [[0,h],[1,h]], #change
                    "Tspot" : 20.5, #change
                    "on" : 1000 #change
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
                SIM_TIME = 3000 #in bee timesteps

                sim = Sim(hive_param,draw_on=True,hotspot=hotspot,draw_t=dr[k]) #the simulation is redrawn every DRAW_T steps
                for i in range(SIM_TIME):
                    sim.update()
                    print(i)

                sim.end()


else:
    bee_param = {
        "Tcoma" : 8,
        "TminI" : 18,
        "TmaxI" : 23,
        "xmax"  : 49,
        "ymax"  : 99,
        "alpha" : 0.01
    }

    hotspot = {
        "coord" : [[0,3],[1,3]], #change
        "Tspot" : 20.5, #change
        "on" : 0, #change
        "off" : 50
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
    }
    SIM_TIME = 100 #in bee timesteps

    sim = Sim(hive_param,draw_on=True,hotspot=hotspot,draw_t=1) #the simulation is redrawn every DRAW_T steps
    for i in tqdm(range(SIM_TIME)):
        sim.update()
        #print(i)

    sim.end()