from cube.rubiks_cube.functions import build_cube, save_cube
from cube.rubiks_cube.controller import RubiksCubeController

import numpy as np

rc = build_cube(signature='test', init='blank')
controller = RubiksCubeController()

for i in range(12):
    controller.initialise_step(rc, np.random.choice(['r', 'g', 'y', 'o', 'b', 'w']))
    save_cube(rc)