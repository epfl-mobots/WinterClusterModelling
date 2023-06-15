# WinterClusterModelling
Winter Cluster Modelling: Semester project carried out during the Spring 2023 semester by Louise Genoud, under the supervision of Dr Rob Mills and Cyril Monette.

## Structure and description
The up-to-date version of the project is on the __explore__ branch. The __main__ branch is an out-of-date version of the Sumpter & Broomhead model replication, and the other branches are tests.

The file structure is the following :

```
WinterClusterModelling 
├── __init__.py
├── README.md
├── analysis
│   ├── __init__.py
│   ├── analyze.py
│   └── plot_temp.py
├── annotation
│   ├── annotate.py
│   ├── compute_surf.py
│   ├── surf_annotate.py
│   └── surf_ellipse.py
└── sumpter
    ├── __init__.py
    ├── bee.py
    ├── draw.py
    ├── hive.py
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

The __sumpter__ subfolder contains the model definition and scripts to run simulations.
- main.py : script to initiate simulations
- sim.py : definition of the Sim class handling the update of the Hive and graphics, as well as saving
- hive.py : definition of the Hive class
- bee.py : definition of the Bee (agent) class
- draw.py : function definitions for graphics rendering

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