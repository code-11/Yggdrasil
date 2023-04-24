import random

import pygame
import sys

import hexes
from terrain import read_terrain_map

pygame.init()
screen = pygame.display.set_mode((640, 480))
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

terrain_map = read_terrain_map(r"C:\Users\brend\Documents\Yggdrasil\assets\terrain_maps\test.png",25,13)
the_map = HexMap(25, 13, terrain_map)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for hex in the_map.hexes:
        screen.blit(hex.image,(hex.x,hex.y))
    pygame.display.update()
