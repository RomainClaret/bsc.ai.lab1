import os, sys

import pygame
from pygame.locals import *
import LittleCity
import geneticAlgoritm as ga

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')


if __name__ == "__main__":
    filename_cities = "data/pb010.txt"

    cities = LittleCity.get_cities(filename_cities)
    #print(cities)

    population_count = 50

    travel_lengths, best_route = ga.find_trip(cities, population_count, ga.use_roulette_selection, ga.improved_greedy_crossover)

    print("Genetic Algorithm")
    print("=================")
    print(" - Roulette Selection")
    print(best_route)
    print(travel_lengths)