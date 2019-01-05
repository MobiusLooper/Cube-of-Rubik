from cube.move import Move
from cube.component_cube.model import ComponentCubeModel

import numpy as np

class ComponentCubeController():
    def __init__(self):
        self.rotation_mapping = {
            'x': {'f': 't', 't': 'k', 'k': 'b', 'b': 'f', 'l': 'l', 'r': 'r'},
            'y': {'f': 'l', 'l': 'k', 'k': 'r', 'r': 'f', 't': 't', 'b': 'b'},
            'z': {'t': 'l', 'l': 'b', 'b': 'r', 'r': 't', 'f': 'f', 'k': 'k'}
        }
        self.position_mapping = {
            '[2, 1]': [1, 0],
            '[1, 0]': [0, 1],
            '[0, 1]': [1, 2],
            '[1, 2]': [2, 1],
            '[0, 0]': [0, 2],
            '[0, 2]': [2, 2],
            '[2, 2]': [2, 0],
            '[2, 0]': [0, 0],
            '[1, 1]': [1, 1]
        }
        self.projections = {
            'x': [1, 2],
            'y': [2, 0],
            'z': [0, 1]
        }

    def make_move(self, cc: ComponentCubeModel, move: Move):
        num_rotations = int(4 * move.rotation)
        assert num_rotations in [1, 2, 3]
        for i in range(num_rotations):
            self.get_new_orientation(cc, move)
            self.get_new_position(cc, move)

    def get_new_orientation(self, cc: ComponentCubeModel, move: Move):
        cc.orientation = {k: cc.orientation[v] for k, v in self.rotation_mapping[move.axis].items()}

    def get_new_position(self, cc: ComponentCubeModel, move: Move):
        position_copy = cc.position.copy()
        projection = self.projections[move.axis]
        projection_coords = [position_copy[projection[0]], position_copy[projection[1]]]
        new_sub_positions = self.position_mapping[str(projection_coords)]
        cc.position[projection[0]] = new_sub_positions[0]
        cc.position[projection[1]] = new_sub_positions[1]