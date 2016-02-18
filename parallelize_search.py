# coding: latin-1


'''
Parallelize search
'''

import time
import threading

import search_params_bruteforce

threads = []


class SearchThread(threading.Thread):
    def __init__(self, _commands):
        threading.Thread.__init__(self)
        self.commands = _commands

    def run(self):
        search_params_bruteforce.main(self.commands)


# PARALLEL
parallel_value = 1

# VALUES
population_size_min = 1
population_size_max = 50
population_size_unit = 1

tournaments_min = 2
tournaments_max = 10
tournaments_unit = 1

elitism_rate_min = 1
elitism_rate_max = 50
elitism_rate_unit = 1

mutation_rate_min = 10
mutation_rate_max = 50
mutation_rate_unit = 10

population_size_part = (population_size_max - population_size_min) / parallel_value
tournaments_part = (tournaments_max - tournaments_min) / parallel_value
elitism_rate_part = (elitism_rate_max - elitism_rate_min) / parallel_value
mutation_rate_part = (mutation_rate_max - mutation_rate_min) / parallel_value

commands = []
for i in range(0, parallel_value):
    parallel_cvs_file_id = i

    parallel_population_size_part = population_size_min + population_size_part * i
    parallel_tournaments_part = population_size_min + tournaments_part * i
    parallel_elitism_rate_part = population_size_min + elitism_rate_part * i
    parallel_mutation_rate_part = population_size_min + mutation_rate_part * i

    parallel_population_size_part_next = population_size_min + population_size_part * (i + 1)
    parallel_tournaments_part_next = population_size_min + tournaments_part * (i + 1)
    parallel_elitism_rate_part_next = population_size_min + elitism_rate_part * (i + 1)
    parallel_mutation_rate_part_next = population_size_min + mutation_rate_part * (i + 1)

    commands.append([parallel_population_size_part,
                     parallel_population_size_part_next,
                     population_size_unit,
                     parallel_tournaments_part,
                     parallel_tournaments_part_next,
                     tournaments_unit,
                     parallel_elitism_rate_part,
                     parallel_elitism_rate_part_next,
                     elitism_rate_unit,
                     parallel_mutation_rate_part,
                     parallel_mutation_rate_part_next,
                     mutation_rate_unit,
                     parallel_cvs_file_id,
                     ])
    print(commands)

try:
    for i in range(0, len(commands)):
        print("Running part " + str(i) + "/" + str(len(commands) - 1))
        thread = SearchThread(commands[i])
        threads.append(thread)
        thread.start()
        time.sleep(1)

except:
    print "Error: unable to start thread"

for t in threads:
    t.join()
print "Exiting Main Thread"

# print(command)

# os.system(command)
# subprocess.Popen(command)

# subprocess.call(["python", "/Users/TimeTraveler/CloneWars/Hot-TSP/search-params-bruteforce.py " +
#                  str(parallel_population_size_part) + " " +
#                  str(parallel_population_size_part_next) + " " +
#                  str(population_size_unit) + " " +
#                  str(parallel_tournaments_part) + " " +
#                  str(parallel_tournaments_part_next) + " " +
#                  str(tournaments_unit) + " " +
#                  str(parallel_elitism_rate_part) + " " +
#                  str(parallel_elitism_rate_part_next) + " " +
#                  str(elitism_rate_unit) + " " +
#                  str(parallel_mutation_rate_part) + " " +
#                  str(parallel_mutation_rate_part_next) + " " +
#                  str(mutation_rate_unit) + " " +
#                  str(parallel_cvs_file_id)])

# os.system("open --new /Applications/Utilities/Terminal.app /usr/bin/python /Users/TimeTraveler/CloneWars/Hot-TSP/search-params-bruteforce.py " +
#              str(parallel_population_size_part) + " " +
#              str(parallel_population_size_part_next) + " " +
#              str(population_size_unit) + " " +
#              str(parallel_tournaments_part) + " " +
#              str(parallel_tournaments_part_next) + " " +
#              str(tournaments_unit) + " " +
#              str(parallel_elitism_rate_part) + " " +
#              str(parallel_elitism_rate_part_next) + " " +
#              str(elitism_rate_unit) + " " +
#              str(parallel_mutation_rate_part) + " " +
#              str(parallel_mutation_rate_part_next) + " " +
#              str(mutation_rate_unit) + " " +
#              str(parallel_cvs_file_id))
