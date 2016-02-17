# coding: latin-1

'''
Cherche les meilleures parametre en brute force...
'''

import collections

module = "Claret_Visinand"
file_name = "data/pb100.txt"
max_time = 20

population_size_min = 100
population_size_max = 200
population_size_unit = 50

tournaments_min = 2
tournaments_max = 10
tournaments_unit = 1

elitism_rate_min = 10
elitism_rate_max = 100
elitism_rate_unit = 10

mutation_rate_min = 10
mutation_rate_max = 100
mutation_rate_unit = 10


# Liste des tests à effectuer 
# sous forme de couples (<datafile>, <maxtime>) où
# <datafile> est le fichier contenant les données du problème et
# <maxtime> le temps (en secondes) imparti pour la résolution
tests = (
    (file_name, max_time),
)

# On tolère un dépassement de 5% du temps imparti:
tolerance = 0.05

# Fichier dans lequel écrire les résultats
import sys
outfile = sys.stdout
# ou :
#outfile = open('results.csv', 'w')

# affichage à la console d'informations d'avancement?
verbose = False

# est-ce qu'on veut un affichage graphique?
gui = False

# PROGRAMME
# =========
# Cette partie n'a théoriquement pas à être modifiée

import os
from time import time
from math import hypot

def dist(city1,city2):
    x1,y1 = city1
    x2,y2 = city2
    return hypot(x2 -x1,y2-y1)

def validate(filename, length, path, duration, maxtime):
    '''Validation de la solution
    
    retourne une chaîne vide si tout est OK ou un message d'erreur sinon
    '''
    error = ""
    
    if duration>maxtime * (1+tolerance):
        error += "Timeout (%.2f) " % (duration-maxtime)
    try:
        cities = dict([(name, (int(x),int(y))) for name,x,y in [l.split() for l in file(filename)]])
    except:
        return "(Validation failed...)"
    tovisit = cities.keys()
    
    try:
        totaldist = 0
        for (ci, cj) in zip(path, path[1:] +path[0:1]):

            totaldist += dist(cities[ci],cities[cj]) #bug here....
            tovisit.remove(ci)
            
        if int(totaldist) != int(length):
            error += "Wrong dist! (%d instead of %d)" % (length, totaldist)
    except KeyError:
        error += "City %s does not exist! " % ci
    except ValueError:
        error += "City %s appears twice in %r! " % (ci, path)
    except Exception as e:
        error += "Error during validation: %r" % e
    
    if tovisit:
        error += "Not all cities visited! %r" % tovisit
    
    return error



if __name__ == '__main__':
    solvers = {}
    top_solutions = {}
    best_solution = [8071, 100, 2, 10, 10]

    exec ("from %s import ga_solve" % module)
    solvers[module] = ga_solve
    outfile.write("%s;" % module)

    outfile.write('\n')



    import csv
    fieldnames = ['length', 'population_size', 'tournaments', 'elitism_rate', 'mutation_rate']
    csvfile = open(str(file_name[5:-4])+'-'+str(max_time)+'.csv', 'w')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    #result = []
    #i=0
    #for population_value in range(population_size_min, population_size_max, population_size_unit):
    #    for tournament_value in range(tournaments_min, tournaments_max, tournaments_unit):
    #        for elitism_rate_value in range(elitism_rate_min, elitism_rate_max, elitism_rate_unit):
    #            for mutation_rate_value in range(mutation_rate_min, mutation_rate_max, mutation_rate_unit):
    #                result.append(++i)

    #print len(result)

    value = len([1+1
              for population_value in range(population_size_min, population_size_max, population_size_unit)
              for tournament_value in range(tournaments_min, tournaments_max, tournaments_unit)
              for elitism_rate_value in range(elitism_rate_min, elitism_rate_max, elitism_rate_unit)
              for mutation_rate_value in range(mutation_rate_min, mutation_rate_max, mutation_rate_unit)
              ])

    print(str(value*max_time/3600) + " h")

    i = 0

    for population_value in range(population_size_min, population_size_max, population_size_unit):
        for tournament_value in range(tournaments_min, tournaments_max, tournaments_unit):
            for elitism_rate_value in range(elitism_rate_min, elitism_rate_max, elitism_rate_unit):
                for mutation_rate_value in range(mutation_rate_min, mutation_rate_max, mutation_rate_unit):
                    i += 1
                    filename = os.path.normcase(os.path.normpath(file_name))
                    outfile.write("%s (%ds), #%d;" % (filename, max_time, i))
                    try:
                        length, path = solvers[module](filename, gui, max_time)
                    except Exception as e:
                        outfile.write("%r;" % e)
                    except SystemExit:
                        outfile.write("tried to quit!;")
                    outfile.write("\n")
                    outfile.flush()

                    writer.writerow({'length': int(length), 'population_size': population_value,
                                     'tournaments': tournament_value, 'elitism_rate': elitism_rate_value,
                                     'mutation_rate': mutation_rate_value
                                     })
                    csvfile.flush()

                    #top_solutions[length] = [population_value, tournament_value, elitism_rate_value, mutation_rate_value]
                    #for key in sorted(top_solutions.iterkeys()):
                    #    print("%s: %s" % (key, top_solutions[key]))

                    print("this: " + str([int(length), population_value, tournament_value, elitism_rate_value, mutation_rate_value]))

                    best_length = best_solution[0]
                    if int(best_length) > int(length):
                        best_solution = [int(length), population_value, tournament_value, elitism_rate_value, mutation_rate_value]
                    print("current best: " + str(best_solution))
                    print("")


    csvfile.close()