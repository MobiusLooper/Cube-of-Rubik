from cube.rubiks_cube.model import RubiksCubeModel
from cube.rubiks_cube.controller import RubiksCubeController
from cube.rubiks_cube.view import RubiksCubeView
from cube.component_cube.model import ComponentCubeModel

import os
import pickle

ORIENTATION_SOLVED = {
    'f': 'f',
    'k': 'k',
    'l': 'l',
    'r': 'r',
    't': 't',
    'b': 'b'
}

ORIENTATION_UNCOLOURED = {
    'f': 'u',
    'k': 'u',
    'l': 'u',
    'r': 'u',
    't': 'u',
    'b': 'u'
}

PERFECTLY_SOLVED_STATE = [
    ComponentCubeModel(position=[i, j, k],
                       orientation=ORIENTATION_SOLVED.copy()) \
    for i in range(3) \
    for j in range(3) \
    for k in range(3)
]

BLANK_STATE = [
    ComponentCubeModel(position=[i, j, k],
                       orientation=ORIENTATION_UNCOLOURED.copy()) \
    for i in range(3) \
    for j in range(3) \
    for k in range(3)
]

controller = RubiksCubeController()
view = RubiksCubeView()


def build_cube(signature: str, init=False):
    if init:
        rc = RubiksCubeModel(signature=signature)
        if init == 'blank':
            rc.apply_state(BLANK_STATE)
            controller.update_face(rc, [0, 0, 0], 'f', 'w')
        elif init_state == 'randomise':
            rc.apply_state(PERFECTLY_SOLVED_STATE)
            controller.randomise(rc)
        elif init_state == 'solved':
            rc.apply_state(PERFECTLY_SOLVED_STATE)

    else:
        path = os.path.join('app', 'saved_states', f'state_{signature}.pkl')
        with open(path, 'rb') as f:
            rc = pickle.load(f)

    return rc


def save_cube(rc: RubiksCubeModel):
    path = os.path.join('app', 'saved_states', f'state_{rc.signature}.pkl')
    with open(path, 'wb') as f:
        pickle.dump(rc, f)
    view.record_state(rc)
