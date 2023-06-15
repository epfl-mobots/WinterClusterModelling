# WinterClusterModelling
Winter Cluster Modelling: Semester project carried out during the Spring 2023 semester by Louise Genoud, under the supervision of Dr Rob Mills and Cyril Monette.

## Structure
The up-to-date version of the project is on the *explore* branch. The *main* branch is an out-of-date version of the Sumpter & Broomhead model replication, and the other branches are tests.

The file structure is the following :

```
WinterClusterModelling 
├── __init__.py
├── README.md
├── analysis
│   ├── __init__.py
│   ├── analyze.py
│   ├── plot_temp.py
├── annotation
│   ├── annotate.py
│   ├── compute_surf.py
│   ├── surf_annotate.py
│   ├── surf_ellipse.py
├── sumpter
│   ├── __init__.py
│   ├── bee.py
│   ├── draw.py
│   ├── hive.py
│   ├── main.py
│   ├── sim_parameters.py
│   ├── sim.py
│   ├── temp_field.py
│   ├── test.py
├── test1
│   ├── funcs.py
│   ├── graph.py
│   ├── test1.py
└── .gitignore 
```

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