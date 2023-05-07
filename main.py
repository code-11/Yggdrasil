import math
import random

import pygame
from pygame.locals import *
import sys

import hexes
from terrain import read_terrain_map

pygame.init()
WINDOW_X = 1024
WINDOW_Y = 768
# WINDOW_X = 400
# WINDOW_Y = 400
screen = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
pygame.display.set_caption("Yggdrasil")

tile_types = [
    "Grass",
    "HillsGreen",
    "Jungle",
    "Mountains"
]

mod_types = [
    "Dirtroad"
]


class HexMap:
    def __init__(self, tiles_width, tiles_height, terrain_map):
        self.tiles_height = tiles_height
        self.tiles_width = tiles_width
        self.hexes = []
        self.modifiers = []
        for x in range(self.tiles_width):
            for y in range(self.tiles_height):
                adjust_up = 0 if x % 2 == 0 else 15
                self.hexes.append(
                    Hex(
                        (x + 1) * 22,
                        (y + 1) * 30 + adjust_up,
                        terrain_map[y][x]
                    )
                )

    def get_col(self, col_index):
        return self.hexes[col_index * self.tiles_height:(col_index + 1) * self.tiles_height]

    def get_row(self, row_index):
        return self.hexes[row_index:len(self.hexes):self.tiles_height]

    def neighbors(self, hex_tile):
        # hex_index = self.hexes.index(hex_tile)
        pass

    def closest_hex(self, pt):
        pt_x, pt_y = pt
        left_col_i, right_col_i = math.floor((pt_x) / 22) - 1, math.ceil((pt_x) / 22) - 1
        # You could do indexing by the row as well and set intersect them, but I'm too lazy to figure it out.
        candidate_hexes = self.get_col(left_col_i) + self.get_col(right_col_i)
        closest = min(candidate_hexes, key=lambda tile_hex: tile_hex.dist(pt))
        return closest

    def add_modifier(self, modifier_name, x, y, index):
        hex_con_indexes = [False] * 6
        hex_con_indexes[index] = True
        # hex_con_indexes[0] = True
        # hex_con_indexes[3] = True
        self.modifiers.append(Modifier(
            x, y, modifier_name, hex_con_indexes
        ))


class Modifier:
    def __init__(self, x, y, mod_type, hex_con_indexes):
        self.x = x
        self.y = y
        self.type = mod_type
        self.hex_con_indexes = hex_con_indexes
        self.images = []

        for i in range(6):
            if self.hex_con_indexes[i]:
                self.images.append(
                    pygame.transform.rotate(
                        pygame.transform.scale(pygame.image.load(hexes.modifier_path(mod_type)),
                                               (Hex.rect_width, Hex.rect_height)),
                        -60 * i
                    )
                )

    def display(self, screen, camera):
        for img in self.images:
            screen.blit(img, (self.x + camera.x, self.y + camera.y))


def dot2(vec1, vec2):
    vec1_x, vec1_y = vec1
    vec2_x, vec2_y = vec2
    return (vec1_x * vec2_x) + (vec1_y * vec2_y)


class Hex:
    rect_height = 30
    rect_width = 30

    @property
    def center_x(self):
        return round(self.x + (Hex.rect_width / 2))

    @property
    def center_y(self):
        return round(self.y + (Hex.rect_height / 2))

    @property
    def center(self):
        return self.center_x, self.center_y

    def dist(self, pt):
        return math.hypot(pt[0] - self.center_x, pt[1] - self.center_y)

    def __init__(self, x, y, tile_type):
        self.x = x
        self.y = y
        self.type = tile_type

        tile_subtype = random.randint(1, 5)
        self.image = pygame.transform.scale(pygame.image.load(hexes.path(tile_type, tile_subtype)),
                                            (Hex.rect_width, Hex.rect_height))

    def draw_debug(self, surface, camera):
        pygame.draw.circle(surface, (255, 0, 255), (self.center_x + camera.x, self.center_y + camera.y), 2)

    def angle_between(self, other_hex):
        diff_x = other_hex.center_x - self.center_x
        diff_y = other_hex.center_y - self.center_y
        return math.degrees(math.atan2(diff_y, diff_x))

    def index_between(self, other_hex):
        forward_angle = self.angle_between(other_hex)
        zero = 0, anglify((0, 0), (0, -Hex.rect_height))
        one = 1, anglify((0, 0), (.75 * Hex.rect_width, -.5 * Hex.rect_height))
        two = 2, anglify((0, 0), (.75 * Hex.rect_width, .5 * Hex.rect_height))
        three = 3, anglify((0, 0), (0, Hex.rect_height))
        four = 4, anglify((0, 0), (-.75 * Hex.rect_width, .5 * Hex.rect_height))
        five = 5, anglify((0, 0), (-.75 * Hex.rect_width, -.5 * Hex.rect_height))
        indexes = [zero, one, two, three, four, five]
        for index in indexes:
            if abs(forward_angle - index[1])<5:
                return index[0]
        return None


def iter_raycast(pt1, pt2, iter_dis=20):
    pt1_x, pt1_y = pt1
    pt2_x, pt2_y = pt2
    displacement_vector = (pt2_x - pt1_x), (pt2_y - pt1_y)
    distance = math.hypot((pt2_x - pt1_x), (pt2_y - pt1_y))
    normed_vector = displacement_vector[0] / distance, displacement_vector[1] / distance
    to_return = []
    for cur_dis in range(0, math.ceil(distance), iter_dis):
        vec_x, vec_y = normed_vector
        cur_pos = pt1_x + (vec_x * cur_dis), pt1_y + (vec_y * cur_dis)
        to_return.append(cur_pos)
    return to_return


class Camera:
    def __init__(self, max_speed):
        self.max_speed = max_speed
        self.x = 0
        self.y = 0

    def handle_movement(self, keys, map_hex_width, map_hex_height, hex_adj_width, hex_height, window_x, window_y):
        if keys[K_a] and self.x + self.max_speed <= 0:
            self.x += self.max_speed
        if keys[K_d] and self.x - self.max_speed + (map_hex_width * (hex_adj_width + 1)) > window_x:
            self.x -= self.max_speed
        if keys[K_w] and self.y + self.max_speed <= 0:
            self.y += self.max_speed
        if keys[K_s] and self.y - self.max_speed + (map_hex_height * (hex_height + 3)) > window_y:
            self.y -= self.max_speed


vec1 = (0, 0)
vec2 = (0, 1)


def anglify(vec1, vec2):
    diff_x = vec2[0] - vec1[0]
    diff_y = vec2[1] - vec1[1]
    return (math.degrees(math.atan2(diff_y, diff_x)))

def inv_hex_index(index):
    if index < 3:
        return index + 3
    else:
        return index - 3

# anglify((0,0),(0,1))
# anglify((0,1),(0,0))
# anglify((0,0),(1,1))
# anglify((1,0),(0,0))
# anglify((0,0),(1,0))
# anglify((0,0),(.75*Hex.rect_width,.5*Hex.rect_height))

terrain_map = read_terrain_map(r"C:\Users\brend\Documents\Yggdrasil\assets\terrain_maps\test.png", 50, 26)
the_map = HexMap(50, 26, terrain_map)
the_camera = Camera(max_speed=4)

selected_hexes = []

while True:
    none_held = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos_x, pos_y = pygame.mouse.get_pos()
            selected_hexes.append(the_map.closest_hex((pos_x - the_camera.x, pos_y - the_camera.y)))
            # the_map.add_modifier("Dirtroad", selected_hex.x, selected_hex.y)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                finalized_selected_hexes = []
                seen_hexes = set()
                for prev_hex, cur_hex in zip(selected_hexes, selected_hexes[1:]):
                    if prev_hex not in seen_hexes:
                        finalized_selected_hexes.append(prev_hex)
                        seen_hexes.add(prev_hex)
                    iter_pts = iter_raycast(prev_hex.center, cur_hex.center)
                    for iter_pt in iter_pts:
                        intermediate_hex = the_map.closest_hex((iter_pt[0] - the_camera.x, iter_pt[1] - the_camera.y))
                        if intermediate_hex not in seen_hexes:
                            finalized_selected_hexes.append(intermediate_hex)
                            seen_hexes.add(intermediate_hex)
                    if cur_hex not in seen_hexes:
                        finalized_selected_hexes.append(cur_hex)
                        seen_hexes.add(cur_hex)
                selected_hexes = finalized_selected_hexes

                for prev_hex, cur_hex in zip(finalized_selected_hexes, finalized_selected_hexes[1:]):
                    hex_pos_index = prev_hex.index_between(cur_hex)
                    inv_index=inv_hex_index(hex_pos_index)

                    the_map.add_modifier("Dirtroad", prev_hex.x, prev_hex.y,hex_pos_index)
                    the_map.add_modifier("Dirtroad", cur_hex.x, cur_hex.y,inv_index)


    keys = pygame.key.get_pressed()

    the_camera.handle_movement(
        keys,
        the_map.tiles_width,
        the_map.tiles_height,
        22,
        Hex.rect_height,
        WINDOW_X,
        WINDOW_Y
    )

    screen.fill((0, 0, 0))
    for hex_tile in the_map.hexes:
        screen.blit(hex_tile.image, (hex_tile.x + the_camera.x, hex_tile.y + the_camera.y))
    for modifier in the_map.modifiers:
        modifier.display(screen, the_camera)

    for hex_tile in selected_hexes:
        hex_tile.draw_debug(screen, the_camera)

    pygame.display.update()

# TODO: Its not perfect. Try far apart points. There's at least two different errors.
# One may be that the raycast is missing hexes.
# The other is a division by zero somehow.