from cube.rubiks_cube.model import RubiksCubeModel

import numpy as np

rc = RubiksCubeModel(init_state='uninitialised')

for i in range(12):
    rc.initialise_step(np.random.choice(['r', 'g', 'y', 'o', 'b', 'w']))