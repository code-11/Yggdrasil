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
    def __init__(self, hex_width, hex_height, terrain_map):
        self.hex_height = hex_height
        self.hex_width = hex_width
        self.hexes = []
        for x in range(self.hex_width):
            for y in range(self.hex_height):
                adjust_up = 0 if x % 2 == 0 else 15
                self.hexes.append(
                    Hex(
                        (x + 1) * 22,
                        (y + 1) * 30 + adjust_up,
                        terrain_map[y][x]
                    )
                )


class Hex:
    rect_height = 30
    rect_width = 30

    def __init__(self, x, y, tile_type):
        self.x = x
        self.y = y
        self.type = tile_type

        tile_subtype = random.randint(1, 5)
        self.image = pygame.transform.scale(pygame.image.load(hexes.path(tile_type, tile_subtype)), (Hex.rect_width, Hex.rect_height))

camera_x = 0
camera_y = 0

camera_vel_x = 0
camera_vel_y = 0

camera_acceleration = .1
camera_deceleration = .2

camera_max_speed = 4

terrain_map = read_terrain_map(r"C:\Users\brend\Documents\Yggdrasil\assets\terrain_maps\test.png",50,26)
the_map = HexMap(50, 26, terrain_map)

while True:
    none_held = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_a] and camera_x + camera_max_speed <= 0:
        camera_x += camera_max_speed
    if keys[K_d] and camera_x - camera_max_speed + (the_map.hex_width * (22 + 1)) > WINDOW_X:
        camera_x -= camera_max_speed
    if keys[K_w] and camera_y + camera_max_speed <= 0:
        camera_y += camera_max_speed
    if keys[K_s] and camera_y - camera_max_speed + (the_map.hex_height * (Hex.rect_height + 3)) >WINDOW_Y:
        camera_y -= camera_max_speed

    screen.fill((0, 0, 0))
    for hex in the_map.hexes:
        screen.blit(hex.image, (hex.x + camera_x, hex.y + camera_y))
    print(f"camera_x: {camera_x}")
    print(f"camera_y: {camera_y}")
    print(f"x: {(the_map.hex_width * (22 + 1)) + camera_x > WINDOW_X}")
    print(f"y: {(the_map.hex_height * (Hex.rect_height + 3)) + camera_y > WINDOW_Y}")

    pygame.display.update()
