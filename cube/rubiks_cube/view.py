from cube.component_cube.view import ComponentCubeView
from cube.rubiks_cube.model import RubiksCubeModel

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import os


class RubiksCubeView():
    def __init__(self):
        self.cc_view = ComponentCubeView()

    def record_state(self, rc: RubiksCubeModel, border_multiplier=0.05):

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
                vertices = self.cc_view.get_vertices(rc[0, i, j], 'l', 'primary', border_multiplier)
                polygon = Polygon(vertices)
                patches.append(polygon)
                colours.append(colourmap[rc[0, i, j].orientation['l']] * 0.9)

        for i in range(3):
            for j in range(3):
                vertices = self.cc_view.get_vertices(rc[i, 2, j], 't', 'primary', border_multiplier)
                polygon = Polygon(vertices)
                patches.append(polygon)
                colours.append(colourmap[rc[i, 2, j].orientation['t']])

        for i in range(3):
            for j in range(3):
                vertices = self.cc_view.get_vertices(rc[i, j, 0], 'f', 'primary', border_multiplier)
                polygon = Polygon(vertices)
                patches.append(polygon)
                colours.append(colourmap[rc[i, j, 0].orientation['f']] * 0.95)

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
                vertices = self.cc_view.get_vertices(rc[2, i, j], 'r', 'secondary', border_multiplier)
                polygon = Polygon(vertices)
                patches.append(polygon)
                colours.append(colourmap[rc[2, i, j].orientation['r']] * 0.9)

        for i in range(3):
            for j in range(3):
                vertices = self.cc_view.get_vertices(rc[i, 0, j], 'b', 'secondary', border_multiplier)
                polygon = Polygon(vertices)
                patches.append(polygon)
                colours.append(colourmap[rc[i, 0, j].orientation['b']] * 0.8)

        for i in range(3):
            for j in range(3):
                vertices = self.cc_view.get_vertices(rc[i, j, 2], 'k', 'secondary', border_multiplier)
                polygon = Polygon(vertices)
                patches.append(polygon)
                colours.append(colourmap[rc[i, j, 2].orientation['k']])

        collection = PatchCollection(patches)
        ax.add_collection(collection)
        collection.set_color(colours)
        plt.xlim([-2.5, 2.5])
        plt.ylim([-0.5, 5.5])
        plt.axis('off')

        plt.savefig(os.path.join('app', 'static', 'saved_state_images', f'cube_state_{rc.signature}.svg'), format='svg')
        plt.close()