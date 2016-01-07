__author__ = 'stevevisinand'

import csv

class LittleCity:
    def __init__ (self, name, posX, posY) :
        self.name = name
        self.posX = posX
        self.posY = posY

    def __str__(self):
        return self.name + "(" + str(self.posX) + ";" + str(self.posY) + ")"

    def __repr__(self):
        return self.name + "(" + str(self.posX) + ";" + str(self.posY) + ")"



def get_data(filename, separator):
    for line in csv.reader(open(filename), delimiter=separator, skipinitialspace=True):
        if line:
            yield line


def get_cities(file):
    cities = []
    for data in get_data(file, ' '):
        chromosomeName = data[0]
        posX = int(data[1])
        posY =  int(data[2])

        city = LittleCity(chromosomeName, posX, posY)
        cities.append(city)

    return cities