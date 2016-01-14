import os, sys

import pygame
from pygame.locals import *
import LittleCity

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')


if __name__ == "__main__":
    filename_cities = "data/pb010.txt"

    cities = LittleCity.get_cities(filename_cities)

    print(cities)