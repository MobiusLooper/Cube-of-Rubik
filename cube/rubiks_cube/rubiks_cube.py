from cube.move import Move
from cube.component_cube.component_cube import ComponentCube
from cube.component_cube.handler import ComponentCubeHandler

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import os
from itertools import product


class RubiksCube():
    def __init__(self, init_state):
        self.solved_orientation = {
            'f': 'f',
            'k': 'k',
            'l': 'l',
            'r': 'r',
            't': 't',
            'b': 'b'
        }
        self.uninitialed_orientation = {
            'f': 'u',
            'k': 'u',
            'l': 'u',
            'r': 'u',
            't': 'u',
            'b': 'u'
        }
        self.colour_to_orientation = {
            'w': 'f',
            'b': 'l',
            'r': 't',
            'y': 'k',
            'o': 'b',
            'g': 'r'
        }

        self.cc_handler = ComponentCubeHandler()

        self.perfectly_solved_state = [
            ComponentCube(position=[i, j, k],
                          orientation=self.solved_orientation) \
            for i in range(3) \
            for j in range(3) \
            for k in range(3)
        ]
        self.uninitialised_state = [
            ComponentCube(position=[i, j, k],
                          orientation=self.uninitialed_orientation.copy()) \
            for i in range(3) \
            for j in range(3) \
            for k in range(3)
        ]

        self.NUM_SMALL_CUBES = 3 * 3 * 3

        self.moves_log = []

        if init_state == 'uninitialised':
            self.state = self.uninitialised_state
            self.initialisation_counter = 0
            self.initialise_step()
        elif init_state == 'randomise':
            self.randomise()
        elif init_state == 'solved':
            self.state = self.perfectly_solved_state
        else:
            raise ValueError("init_state must be one of: uninitialised, randomise, solved")

        self.record_state()

    def randomise(self):
        self.state = self.perfectly_solved_state
        for i in range(100):
            random_move = Move(
                axis=np.random.choice(['x', 'y', 'z']),
                level=np.random.choice([0, 1, 2]),
                rotation=np.random.choice([0.25, 0.5, 0.75])
            )
            self.make_move(random_move)

    def get_cube_positions_to_move(self, move: Move):
        if move.axis == 'x':
            return [[move.level, i, j] for i in range(3) for j in range(3)]
        elif move.axis == 'y':
            return [[i, move.level, j] for i in range(3) for j in range(3)]
        elif move.axis == 'z':
            return [[i, j, move.level] for i in range(3) for j in range(3)]

    def make_move(self, move: Move):
        for i in range(self.NUM_SMALL_CUBES):
            if self.state[i].position in self.get_cube_positions_to_move(move):
                self.cc_handler.make_move(self.state[i], move)
                self.moves_log.append(move)

    def solve(self) -> list:
        pass

    def is_solved(self):
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

        each_side_num_unique = [len(set(face)) for face in all_faces]
        return each_side_num_unique == [1, 1, 1, 1, 1, 1]

    def __getitem__(self, ix):
        return [cc for cc in self.state if cc.position == list(ix)][0]

    def record_state(self, border_multiplier=0.05):

        fig = plt.figure(figsize=[14, 6])

        colourmap = {
            'f': np.array([220, 220, 220]) / 256,  # light grey
            'l': np.array([16, 173, 249]) / 256,  # blue
            't': np.array([249, 40, 16]) / 256,  # red
            'r': np.array([16, 249, 32]) / 256,  # green
            'k': np.array([223, 249, 16]) / 256,  # yellow
            'b': np.array([249, 145, 16]) / 256,  # orange
            'u': np.array([100, 100, 100]) / 256,  # dark grey
            'w': np.array([256, 256, 256]) / 256,  # white
        }

        ax = fig.add_subplot(1, 2, 1)
        patches = []
        colours = []

        for i in range(3):
            for j in range(3):
                vertices = self.cc_handler.get_vertices(self[0, i, j], 'l', 'primary', border_multiplier)
                polygon = Polygon(vertices)
                patches.append(polygon)
                colours.append(colourmap[self[0, i, j].orientation['l']] * 0.9)

        for i in range(3):
            for j in range(3):
                vertices = self.cc_handler.get_vertices(self[i, 2, j], 't', 'primary', border_multiplier)
                polygon = Polygon(vertices)
                patches.append(polygon)
                colours.append(colourmap[self[i, 2, j].orientation['t']])

        for i in range(3):
            for j in range(3):
                vertices = self.cc_handler.get_vertices(self[i, j, 0], 'f', 'primary', border_multiplier)
                polygon = Polygon(vertices)
                patches.append(polygon)
                colours.append(colourmap[self[i, j, 0].orientation['f']] * 0.95)

        collection = PatchCollection(patches)
        ax.add_collection(collection)
        collection.set_color(colours)
        plt.xlim([-2.5, 2.5])
        plt.ylim([-0.5, 5.5])
        plt.axis('off')

        ax = fig.add_subplot(1, 2, 2)
        patches = []
        colours = []

        for i in range(3):
            for j in range(3):
                vertices = self.cc_handler.get_vertices(self[2, i, j], 'r', 'secondary', border_multiplier)
                polygon = Polygon(vertices)
                patches.append(polygon)
                colours.append(colourmap[self[2, i, j].orientation['r']] * 0.9)

        for i in range(3):
            for j in range(3):
                vertices = self.cc_handler.get_vertices(self[i, 0, j], 'b', 'secondary', border_multiplier)
                polygon = Polygon(vertices)
                patches.append(polygon)
                colours.append(colourmap[self[i, 0, j].orientation['b']] * 0.8)

        for i in range(3):
            for j in range(3):
                vertices = self.cc_handler.get_vertices(self[i, j, 2], 'k', 'secondary', border_multiplier)
                polygon = Polygon(vertices)
                patches.append(polygon)
                colours.append(colourmap[self[i, j, 2].orientation['k']])

        collection = PatchCollection(patches)
        ax.add_collection(collection)
        collection.set_color(colours)
        plt.xlim([-2.5, 2.5])
        plt.ylim([-0.5, 5.5])
        plt.axis('off')

        plt.savefig(os.path.join('app', 'static', 'saved_state_images', 'cube_state.svg'), format='svg')
        plt.close()

    def update_face(self, position: list, face: str, colour: str):
        assert face in ['f', 'l', 't', 'r', 'b', 'k'], 'Invalid face'
        assert colour in ['f', 'l', 't', 'r', 'b', 'k', 'w']
        self[tuple(position)].orientation[face] = colour
        self.record_state()

    def initialise_step(self, colour=None):
        assert not self.is_initialised(), "Cube already initialised"
        schedule = list(product(range(3), range(3)))
        schedule = [[s[0], s[1], 0] for s in schedule]
        point_in_schedule = self.initialisation_counter % 9
        if self.initialisation_counter:
            self.update_face(position=schedule[point_in_schedule - 1], face='f',
                             colour=self.colour_to_orientation[colour])
        self.initialisation_rotation()
        if self.initialisation_counter < 54:
            self.update_face(position=schedule[point_in_schedule], face='f', colour='w')
        self.initialisation_counter += 1

    def initialisation_rotation(self):
        if self.initialisation_counter in [9, 18, 27]:
            self.make_move(Move(axis='y', level=0, rotation=0.75))
            self.make_move(Move(axis='y', level=1, rotation=0.75))
            self.make_move(Move(axis='y', level=2, rotation=0.75))
        if self.initialisation_counter == 36:
            self.make_move(Move(axis='x', level=0, rotation=0.75))
            self.make_move(Move(axis='x', level=1, rotation=0.75))
            self.make_move(Move(axis='x', level=2, rotation=0.75))
        if self.initialisation_counter == 45:
            self.make_move(Move(axis='x', level=0, rotation=0.5))
            self.make_move(Move(axis='x', level=1, rotation=0.5))
            self.make_move(Move(axis='x', level=2, rotation=0.5))

    def is_initialised(self):
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

        num_uninitialised = sum([face.count('u') + face.count('w') for face in all_faces])
        initialised = (num_uninitialised == 0)
        if initialised:
            assert self.initialisation_counter == 55
        else:
            assert self.initialisation_counter != 55

        return initialised

    def is_valid_configuration(self):
        pass