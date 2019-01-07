from cube.move import Move
from cube.component_cube.view import ComponentCubeView
from cube.component_cube.controller import ComponentCubeController
from cube.rubiks_cube.view import RubiksCubeView
from cube.rubiks_cube.model import RubiksCubeModel

import numpy as np
from itertools import product


class RubiksCubeController():
    def __init__(self):

        self.COLOUR_TO_ORIENTATION = {
            'w': 'f',
            'b': 'l',
            'r': 't',
            'y': 'k',
            'o': 'b',
            'g': 'r'
        }

        self.cc_view = ComponentCubeView()
        self.cc_controller = ComponentCubeController()
        self.rc_view = RubiksCubeView()

    def randomise(self, rc: RubiksCubeModel):
        for i in range(100):
            random_move = Move(
                axis=np.random.choice(['x', 'y', 'z']),
                level=np.random.choice([0, 1, 2]),
                rotation=np.random.choice([0.25, 0.5, 0.75])
            )
            self.make_move(rc, random_move)

    def get_cube_positions_to_move(self, move: Move):
        if move.axis == 'x':
            return [[move.level, i, j] for i in range(3) for j in range(3)]
        elif move.axis == 'y':
            return [[i, move.level, j] for i in range(3) for j in range(3)]
        elif move.axis == 'z':
            return [[i, j, move.level] for i in range(3) for j in range(3)]

    def make_move(self, rc: RubiksCubeModel, move: Move):
        for i in range(rc.NUM_SMALL_CUBES):
            if rc.state[i].position in self.get_cube_positions_to_move(move):
                self.cc_controller.make_move(rc.state[i], move)
                rc.moves_log.append(move)

    def update_face(self, rc: RubiksCubeModel, position: list, face: str, colour: str):
        assert face in ['f', 'l', 't', 'r', 'b', 'k'], 'Invalid face'
        assert colour in ['f', 'l', 't', 'r', 'b', 'k', 'w']
        rc[tuple(position)].orientation[face] = colour

    def initialise_step(self, rc: RubiksCubeModel, colour=None):
        assert rc.num_coloured() < 54, "Cube already initialised"
        schedule = list(product(range(3), range(3)))
        schedule = [[s[0], s[1], 0] for s in schedule]
        step_now = rc.num_coloured() % 9
        step_next = (rc.num_coloured() + 1) % 9
        print(colour)
        self.update_face(rc, position=schedule[step_now], face='f',
                         colour=self.COLOUR_TO_ORIENTATION[colour])
        self.initialisation_rotation(rc)
        if rc.num_coloured() < 54:
            self.update_face(rc, position=schedule[step_next], face='f', colour='w')

    def initialisation_rotation(self, rc: RubiksCubeModel):
        if rc.num_coloured() in [9, 18, 27]:
            self.make_move(rc, Move(axis='y', level=0, rotation=0.75))
            self.make_move(rc, Move(axis='y', level=1, rotation=0.75))
            self.make_move(rc, Move(axis='y', level=2, rotation=0.75))
        if rc.num_coloured() == 36:
            self.make_move(rc, Move(axis='x', level=0, rotation=0.75))
            self.make_move(rc, Move(axis='x', level=1, rotation=0.75))
            self.make_move(rc, Move(axis='x', level=2, rotation=0.75))
        if rc.num_coloured() == 45:
            self.make_move(rc, Move(axis='x', level=0, rotation=0.5))
            self.make_move(rc, Move(axis='x', level=1, rotation=0.5))
            self.make_move(rc, Move(axis='x', level=2, rotation=0.5))
