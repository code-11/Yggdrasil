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

class HexMap:
    def __init__(self, tiles_width, tiles_height, terrain_map):
        self.tiles_height = tiles_height
        self.tiles_width = tiles_width
        self.hexes = []
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
        return self.hexes[col_index * self.tiles_height:(col_index+1) * self.tiles_height]

    def get_row(self, row_index):
        return self.hexes[row_index:len(self.hexes):self.tiles_height]

    def neighbors(self, hex_tile):
        # hex_index = self.hexes.index(hex_tile)
        pass

    def closest_hex(self, pt):
        pt_x, pt_y = pt
        left_col_i, right_col_i = math.floor((pt_x)/ 22)-1, math.ceil((pt_x) / 22)-1
        # You could do indexing by the row as well and set intersect them, but I'm too lazy to figure it out.
        candidate_hexes = self.get_col(left_col_i) + self.get_col(right_col_i)
        closest = min(candidate_hexes, key=lambda tile_hex: tile_hex.dist(pt))
        return closest


class Hex:
    rect_height = 30
    rect_width = 30

    @property
    def center_x(self):
        return round(self.x + (Hex.rect_width / 2))

    @property
    def center_y(self):
        return round(self.y + (Hex.rect_height / 2))

    def dist(self, pt):
        return math.hypot(pt[0]-self.center_x, pt[1]-self.center_y)

    def __init__(self, x, y, tile_type):
        self.x = x
        self.y = y
        self.type = tile_type

        tile_subtype = random.randint(1, 5)
        self.image = pygame.transform.scale(pygame.image.load(hexes.path(tile_type, tile_subtype)), (Hex.rect_width, Hex.rect_height))

    def draw_debug(self, surface, camera):
        pygame.draw.circle(surface, (255, 0, 255), (self.center_x + camera.x, self.center_y + camera.y), 2)


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


terrain_map = read_terrain_map(r"C:\Users\brend\Documents\Yggdrasil\assets\terrain_maps\test.png",50,26)
the_map = HexMap(50, 26, terrain_map)
the_camera = Camera(max_speed=4)

selected_hex=None

while True:
    none_held = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos_x,pos_y = pygame.mouse.get_pos()
            selected_hex = the_map.closest_hex((pos_x - the_camera.x, pos_y - the_camera.y))
            print(selected_hex.type)

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

    if selected_hex:
        selected_hex.draw_debug(screen,the_camera)

    pygame.display.update()
