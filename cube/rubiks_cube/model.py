from cube.component_cube.model import ComponentCubeModel


class RubiksCubeModel():
    def __init__(self, signature: str):

        self.NUM_SMALL_CUBES = 3 * 3 * 3
        self.moves_log = []
        self.signature = signature

    def __getitem__(self, ix):
        return [cc for cc in self.state if cc.position == list(ix)][0]

    def apply_state(self, state):
        self.state = state

    def is_valid_configuration(self):
        pass

    def num_coloured(self):
        face_left = [cc.orientation['l'] for cc in self.state if cc.position[0] == 0]
        face_right = [cc.orientation['r'] for cc in self.state if cc.position[0] == 2]
        face_bottom = [cc.orientation['b'] for cc in self.state if cc.position[1] == 0]
        face_top = [cc.orientation['t'] for cc in self.state if cc.position[1] == 2]
        face_front = [cc.orientation['f'] for cc in self.state if cc.position[2] == 0]
        face_back = [cc.orientation['k'] for cc in self.state if cc.position[2] == 2]

        all_faces = [
            face_left,
            face_right,
            face_bottom,
            face_top,
            face_front,
            face_back
        ]

        num_blank = sum([face.count('u') + face.count('w') for face in all_faces])
        num_coloured = 6 * 9 - num_blank
        return num_coloured