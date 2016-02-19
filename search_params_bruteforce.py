# coding: latin-1

'''
Cherche les meilleures parametre en brute force...
'''

import sys
import os
import time
from math import hypot
import sys
import csv


module = "Claret_Visinand"
file_name = "data/pb100.txt"
max_time = 20

# population_size_min = 2
# population_size_max = 5
# population_size_unit = 1
#
# tournaments_min = 2
# tournaments_max = 10
# tournaments_unit = 1
#
# elitism_rate_min = 10
# elitism_rate_max = 100
# elitism_rate_unit = 10
#
# mutation_rate_min = 10
# mutation_rate_max = 100
# mutation_rate_unit = 10


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

def dist(city1,city2):
    x1,y1 = city1
    x2,y2 = city2
    return hypot(x2 -x1,y2-y1)

def main(_commands=None):

    if _commands is not None:
        global population_size_min
        population_size_min = _commands[0]
        global population_size_max
        population_size_max = _commands[1]
        global population_size_unit
        population_size_unit = _commands[2]

        global tournaments_min
        tournaments_min = _commands[3]
        global tournaments_max
        tournaments_max = _commands[4]
        global tournaments_unit
        tournaments_unit = _commands[5]

        global elitism_rate_min
        elitism_rate_min = _commands[6]
        global elitism_rate_max
        elitism_rate_max = _commands[7]
        global elitism_rate_unit
        elitism_rate_unit = _commands[8]

        global mutation_rate_min
        mutation_rate_min = _commands[9]
        global mutation_rate_max
        mutation_rate_max = _commands[10]
        global mutation_rate_unit
        mutation_rate_unit = _commands[11]

        cvs_file_id = _commands[12] + 1

    solvers = {}
    top_solutions = {}
    best_solution = [8071, 100, 2, 10, 10]

    exec ("from %s import ga_solve" % module)
    solvers[module] = ga_solve
    outfile.write("%s;" % module)

    outfile.write('\n')

    fieldnames = ['length', 'population_size', 'tournaments', 'elitism_rate', 'mutation_rate',
                  'population_size_min', 'population_size_max', 'population_size_unit',
                  'tournaments_min', 'tournaments_max', 'tournaments_unit',
                  'elitism_rate_min', 'elitism_rate_max', 'elitism_rate_unit',
                  'mutation_rate_min', 'mutation_rate_max', 'mutation_rate_unit']

    timestamp = str(cvs_file_id) + "-" + str(hash(time.ctime(time.time())))
    csvfile = open(str(file_name[5:-4])+'-'+str(max_time)+'-'+str(timestamp)+'.csv', 'w')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({
        'population_size_min': int(population_size_min), 'population_size_max': int(population_size_max),
        'population_size_unit': int(population_size_unit), 'tournaments_min': int(tournaments_min),
        'tournaments_max': int(tournaments_max), 'tournaments_unit': int(tournaments_unit),
        'elitism_rate_min': int(elitism_rate_min), 'elitism_rate_max': int(elitism_rate_max),
        'elitism_rate_unit': int(elitism_rate_unit), 'mutation_rate_min': int(mutation_rate_min),
        'mutation_rate_max': int(mutation_rate_max), 'mutation_rate_unit': int(mutation_rate_unit)
    })

    csvfile.flush()

    value = len([1+1
              for population_value in range(population_size_min, population_size_max+population_size_unit, population_size_unit)
              for tournament_value in range(tournaments_min, tournaments_max+tournaments_unit, tournaments_unit)
              for elitism_rate_value in range(elitism_rate_min, elitism_rate_max+elitism_rate_unit, elitism_rate_unit)
              for mutation_rate_value in range(mutation_rate_min, mutation_rate_max+mutation_rate_unit, mutation_rate_unit)
              ])

    print(str(value*max_time/3600) + " h")
    print(str(value) + " iterations")

    i = 0

    for population_value in range(population_size_min, population_size_max+population_size_unit, population_size_unit):
        for tournament_value in range(tournaments_min, tournaments_max+tournaments_unit, tournaments_unit):
            for elitism_rate_value in range(elitism_rate_min, elitism_rate_max+elitism_rate_unit, elitism_rate_unit):
                for mutation_rate_value in range(mutation_rate_min, mutation_rate_max+mutation_rate_unit, mutation_rate_unit):
                    i += 1
                    filename = os.path.normcase(os.path.normpath(file_name))
                    outfile.write("Thread#%d for %s (%ds), #%d;" % (cvs_file_id, filename, max_time, i))
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

                    print("this: " + str([int(length), population_value, tournament_value, elitism_rate_value, mutation_rate_value]))

                    best_length = best_solution[0]
                    if int(best_length) > int(length):
                        best_solution = [int(length), population_value, tournament_value, elitism_rate_value, mutation_rate_value]
                    print("current best: " + str(best_solution))
                    print("")

    csvfile.close()


if __name__ == '__main__':

    cvs_file_id = 0

    population_size_min = 2
    population_size_max = 5
    population_size_unit = 1

    tournaments_min = 2
    tournaments_max = 10
    tournaments_unit = 1

    elitism_rate_min = 1
    elitism_rate_max = 2
    elitism_rate_unit = 1

    mutation_rate_min = 10
    mutation_rate_max = 60
    mutation_rate_unit = 10

    if len(sys.argv) > 1:
        population_size_min = int(sys.argv[1])
        population_size_max = int(sys.argv[2])
        population_size_unit = int(sys.argv[3])

        tournaments_min = int(sys.argv[4])
        tournaments_max = int(sys.argv[5])
        tournaments_unit = int(sys.argv[6])

        elitism_rate_min = int(sys.argv[7])
        elitism_rate_max = int(sys.argv[8])
        elitism_rate_unit = int(sys.argv[9])

        mutation_rate_min = int(sys.argv[10])
        mutation_rate_max = int(sys.argv[11])
        mutation_rate_unit = int(sys.argv[12])


    commands = [population_size_min,
                     population_size_max,
                     population_size_unit,
                     tournaments_min,
                     tournaments_max,
                     tournaments_unit,
                     elitism_rate_min,
                     elitism_rate_max,
                     elitism_rate_unit,
                     mutation_rate_min,
                     mutation_rate_max,
                     mutation_rate_unit,
                     cvs_file_id,
                     ]
    main(commands)