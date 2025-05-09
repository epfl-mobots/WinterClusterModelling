# Introduction
Winter Cluster Modelling: an agent-based model to model honeybee cluster movements and thermal gradients. Based on [1] and further developed to include shivering [2] with the goal of testing winter cluster transitions as observed by [3].

Model initated as an EPFL semester project carried out by Louise Genoud (Spring 2023), under the supervision of Dr Rob Mills and Cyril Monette. The model was further developed by Clara Wetzel in another EPFL semester project (Fall 2024).

# Structure and description
The up-to-date version of the project is on the __shivering__ branch. This branch needs to be run with a config file having a similar layout than "sumpter_new.cfg", and gives the option of activating shivering thermogenesis, explorer behaviors hypothesis and 3D diffusion. Also, the code's output can be chosen to be given in a relalistic or free frame.

The __TempExp__  branch can be used to characterize and plot the error occuring when temperatures become too high, creating infinite value resulting in an error in the simulation.

The __Sumpter__  branch contains the more recent version of the code containing only Sumpter hypothesis and the implementation of the explorer behaviour coded by Louise Genoud.

The __explore__ branch is an out of date version of the explorer behavior.

The __main__ branch is an out-of-date version of the Sumpter & Broomhead model replication, and the other branches are tests.

The file structure is the following :

```
WinterClusterModelling 
├── __init__.py
├── README.md
├── analysis
│   ├── __init__.py
│   ├── analyze.py
│   └── plot_temp.py
├── Development
│   └── parameters.ipynb
├── annotation
│   ├── annotate.py
│   ├── compute_surf.py
│   ├── surf_annotate.py
│   └── surf_ellipse.py
└── src
    ├── __init__.py
    ├── bee.py
    ├── draw.py
    ├── frame.py
    ├── main.py
    └── sim.py

```
The __analysis__ subfolder contains scripts to generate plots after a simulation has been run (temperature profile and agent distribution).
- analyze.py : main script
- plot_temp.py : helper function definition

The __annotation__ subfolder contains tools to perfom frame annotation from videos.
- annotate.py : frame-by-frame annotation of bee position
- surf_annotate.py and surf_ellipse.py : frame-by-frame annotation of cluster surfaces with ellipses
- compute_surf.py : computation of cluster surfaces from results of annotation with surf_annotate or surf_ellipse

The __src__ subfolder contains the model definition and scripts to run simulations.
- main.py : script to initiate simulations
- sim.py : definition of the Sim class handling the update of the Hive and graphics, as well as saving
- frame.py : definition of the Frame class
- bee.py : definition of the Bee (agent) class
- draw.py : function definitions for graphics rendering

The __Development__ subfolder contains the file "parameters.ipynb" which can be used to compute some parameters used in functions related to the implementation of shivering thermogenesis. These parameters needs to be recomputed and modified in the cfg file if the probability of leaving the active state or if the coma temperature parameters are changed.

## Required libraries
- cv2
- datetime
- gc
- glob
- math
- matplotlib
- numpy
- pickle
- random
- tqdm
- sys

Developed on Python 3.9

# References

[1] D. Sumpter and D. Broomhead, “Shape and dynamics of thermoregulating honey bee clusters,” Journal of Theoretical Biology, vol. 204, pp. 1–14, May 2000.

[2] A. Stabentheiner, H. Pressl, T. Papst, N. Hrassnigg, and K. Crailsheim, “Endothermic heat production in honeybee winter clusters,” Journal of Experimental Biology, vol. 206, pp. 353–358, Jan. 2003.

[3] R. Barmak, M. Stefanec, D. N. Hofstadler, L. Piotet, S. Sch ̈onwetter-Fuchs-Schistek, F. Mondada, T. Schmickl, and R. Mills, “A robotic honeycomb for interaction with a honeybee colony,” Science Robotics, vol. 8, no. 76, 2023.