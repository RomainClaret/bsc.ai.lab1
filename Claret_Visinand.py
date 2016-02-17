import os, sys

#import pygame
#from pygame.locals import *
import littleCity
import drMaboule
import geneticAlgoritm as ga
import transgenicBanana as tb
import time

#if not pygame.font:
#    print('Warning, fonts disabled')
#if not pygame.mixer:
#    print('Warning, sound disabled')


if __name__ == "__main__":
    print()
    print("=== STEVE ===")
    filename_cities = "data/pb010.txt"

    cities = littleCity.get_cities(filename_cities)
    print(cities)

    doctor = drMaboule.DrMaboule(cities)


    print("cities : ", cities)
    print("bestPath : ", doctor.work(100))

    # print()
    # print()
    # print("=== ROMAIN PROTO ===")
    #
    # population_count = 50
    #
    # travel_lengths, best_route = ga.find_trip(cities, population_count, ga.use_roulette_selection, ga.improved_greedy_crossover)
    #
    # print("Genetic Algorithm")
    # print("=================")
    # print(" - Roulette Selection")
    # print(best_route)
    # print(travel_lengths)

    print()
    print()
    print("=== ROMAIN FINAL ===")
    data_filename = "pb010.txt"
    number_of_tests = 2

    nodes_distances_dict = tb.data_parser('data/' + data_filename)
    for test in range(1, number_of_tests + 1):
        print()
        print()
        print('Test #' + str(test))
        start_time = time.perf_counter()
        tb.create_ultimate_banana(nodes_distances_dict, _verbose=False)
        print("Time Elapsed: ", time.perf_counter() - start_time)


