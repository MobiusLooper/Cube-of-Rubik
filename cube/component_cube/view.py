from cube.component_cube.model import ComponentCubeModel

import numpy as np

class ComponentCubeView():
    def __init__(self):
        pass

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