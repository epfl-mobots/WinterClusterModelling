"""Script to initiate simulations and set the parameters."""
from tqdm import tqdm
from argparse import ArgumentParser
import os
import configparser

from sim import Sim


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

def script_parser():
    ''' construct argparse object to interpret the incoming command '''
    parser = ArgumentParser(exit_on_error=True)
    parser.add_argument('-c', '--cfg', help='path to config file')
    parser.add_argument('-f', '--frame', help='path to frame file')
    return parser

def verify_cfg_file(cfg_path): 
    ''' Check if config file exists '''
    relative_path="../configs/"+cfg_path
    abs_path=os.path.realpath(relative_path)
    if not os.path.isfile(abs_path):
        raise FileNotFoundError(f"No config file found at '{abs_path}'") 
    
    cfg = configparser.ConfigParser()
    cfg.read(abs_path)  # abs_path is a canonical path

    if len(cfg.sections())!=4:
        raise configparser.ParsingError(f"Invalid number of sections: {cfg.sections()}")
    if 'bee' not in cfg or 'hive' not in cfg or 'hotspot' not in cfg or 'simu' not in cfg:
        raise configparser.ParsingError(f"Could not find the expected sections: bee, hive, hotspot, simu")
    
    return abs_path

if __name__ == "__main__":
    parser=script_parser()
    args = parser.parse_args()
    abs_cfg_path=None

    if args.cfg is not None:
        abs_cfg_path=verify_cfg_file(str(args.cfg))

    sim = Sim(cfg_path=abs_cfg_path, frame_save=args.frame)
    
    simu_steps=sim.simu_steps
    save_freq=sim.save_freq

    print("Starting simulation.")
    for i in tqdm(range(simu_steps)):
        sim.update()
        if i%save_freq==0:
            sim.save()
        
    sim.end()
    print(f"Simulation finished.")