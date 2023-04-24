# Imports PIL module
import random

import numpy
from PIL import Image
from numpy import asarray, array



class TileChooser(object):
    def __init__(self, list_o_ranges):
        self.inner_data = list_o_ranges

    def floor_val(self, num):
        prev = self.inner_data[0][0]
        for range in self.inner_data:
            if num <= range[0]:
                return prev
            prev = range

    def choose(self, num):
        floor_val, choices = self.floor_val(num)
        return random.choice(choices)


def extract_avg(img, x, y, n=3):
    square = img.crop((x-n+1, y-n+1, x+n, y+n))
    square_pixels = list(square.getdata())
    r_channel = list(zip(*square_pixels))[0]
    average = sum(r_channel) / len(r_channel)
    return average


def read_terrain_map(file, grid_width, grid_height):
    the_chooser = TileChooser([
        (0, ["Water"]),
        (45, ["Water", "Swamp"]),
        (60, ["Swamp"]),
        (70, ["Jungle", "Jungle", "Grass"]),
        (140, ["HillsGreen"]),
        (170, ["Mountains"]),
        (256, [None])
    ])

    img = Image.open(file).convert("RGB")
    pixels = img.load()
    x_shift = img.size[0]/(grid_width+1)
    y_shift = img.size[1]/(grid_height+1)

    to_return = []
    for j in range(grid_height):
        tile_row = []
        for i in range(grid_width):
            x_pos = int((i+1)*x_shift)
            y_pos = int((j+1)*y_shift)
            avg_val = extract_avg(img, x_pos, y_pos)
            tile_row.append(the_chooser.choose(avg_val))
        to_return.append(tile_row)
    return to_return


