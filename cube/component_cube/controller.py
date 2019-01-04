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

    def get_vertices(self, cc: ComponentCubeModel, face, view, border_multiplier):

        bm = border_multiplier

        x = np.array([0.8, 0.13])
        y = np.array([0, 1])
        z = np.array([-0.3, 0.4])

        if view == 'primary':

            if face == 'f':
                bl_coords = [cc.position[0] * x, cc.position[1] * y, x * bm, y * bm]
                tl_coords = [cc.position[0] * x, (cc.position[1] + 1) * y, x * bm, -y * bm]
                tr_coords = [(cc.position[0] + 1) * x, (cc.position[1] + 1) * y, -x * bm, -y * bm]
                br_coords = [(cc.position[0] + 1) * x, cc.position[1] * y, -x * bm, y * bm]
            elif face == 't':
                bl_coords = [cc.position[0] * x, 3 * y, cc.position[2] * z, x * bm, z * bm]
                tl_coords = [cc.position[0] * x, 3 * y, (cc.position[2] + 1) * z, x * bm, -z * bm]
                tr_coords = [(cc.position[0] + 1) * x, 3 * y, (cc.position[2] + 1) * z, -x * bm, -z * bm]
                br_coords = [(cc.position[0] + 1) * x, 3 * y, cc.position[2] * z, -x * bm, z * bm]
            elif face == 'l':
                bl_coords = [cc.position[1] * y, (cc.position[2] + 1) * z, y * bm, -z * bm]
                tl_coords = [(cc.position[1] + 1) * y, (cc.position[2] + 1) * z, -y * bm, -z * bm]
                tr_coords = [(cc.position[1] + 1) * y, cc.position[2] * z, -y * bm, z * bm]
                br_coords = [cc.position[1] * y, cc.position[2] * z, y * bm, z * bm]
            else:
                raise IndexError(f"Face '{face}' not valid with view '{view}'")

            UPWARD_ADJUSTMENT = np.array([0, 0])

        elif view == 'secondary':

            x = x * np.array([1, -1])
            z = z * np.array([1, -1])

            if face == 'k':
                bl_coords = [(2 - cc.position[0]) * x, cc.position[1] * y, x * bm, y * bm]
                tl_coords = [(2 - cc.position[0]) * x, (cc.position[1] + 1) * y, x * bm, -y * bm]
                tr_coords = [(3 - cc.position[0]) * x, (cc.position[1] + 1) * y, -x * bm, -y * bm]
                br_coords = [(3 - cc.position[0]) * x, cc.position[1] * y, -x * bm, y * bm]
            elif face == 'b':
                bl_coords = [(2 - cc.position[0]) * x, (3 - cc.position[2]) * z, x * bm, -z * bm]
                tl_coords = [(2 - cc.position[0]) * x, (2 - cc.position[2]) * z, x * bm, z * bm]
                tr_coords = [(3 - cc.position[0]) * x, (2 - cc.position[2]) * z, -x * bm, z * bm]
                br_coords = [(3 - cc.position[0]) * x, (3 - cc.position[2]) * z, -x * bm, -z * bm]
            elif face == 'r':
                bl_coords = [cc.position[1] * y, (3 - cc.position[2]) * z, y * bm, -z * bm]
                tr_coords = [(cc.position[1] + 1) * y, (2 - cc.position[2]) * z, -y * bm, z * bm]
                tl_coords = [(cc.position[1] + 1) * y, (3 - cc.position[2]) * z, -y * bm, -z * bm]
                br_coords = [cc.position[1] * y, (2 - cc.position[2]) * z, y * bm, z * bm]
            else:
                raise IndexError(f"Face '{face}' not valid with view '{view}'")

            UPWARD_ADJUSTMENT = np.array([0, (x[1] + y[1]) * 2])

        else:
            raise IndexError(f"View '{view}' not valid")

        bl = sum(bl_coords) + UPWARD_ADJUSTMENT
        tl = sum(tl_coords) + UPWARD_ADJUSTMENT
        tr = sum(tr_coords) + UPWARD_ADJUSTMENT
        br = sum(br_coords) + UPWARD_ADJUSTMENT

        return [bl, tl, tr, br]