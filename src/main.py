"""Script to initiate simulations and set the parameters."""
from tqdm import tqdm
from argparse import ArgumentParser
import os
import configparser

from sim import Sim

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

    if len(cfg.sections())!=7:
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