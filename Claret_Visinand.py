import os, sys
import csv
import pygame
from pygame.locals import *

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

def get_data(filename, separator):
    for line in csv.reader(open(filename), delimiter=separator, skipinitialspace=True):
        if line:
            yield line


def get_positions(file):
    positions = {}
    for data in get_data(file, ' '):
        positions[data[0]] = (int(data[1]), int(data[2]))
    return positions

def get_graph(file, positions):
    graph = {}
    for data in get_data(file, ' '):
        if data[0] in graph:
            graph[data[0]].update([(data[1], int(data[2]))])
        else:
            graph[data[0]] = set([(data[1], int(data[2]))])

    for check_data in positions:
        if check_data not in graph:
            graph[check_data] = set([])

    for key in graph:
        for value in graph[key]:
            graph[value[0]].update([(key, value[1])])

    return graph