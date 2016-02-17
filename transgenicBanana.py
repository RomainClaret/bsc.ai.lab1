__author__ = 'Romain Claret'

# Use of dictionaries instead of lists for performance O(n) vs O(1), we are mainly doing key-value here

import math
import time
import random
import drMaboule
from collections import OrderedDict


class TransgenicBanana:
    def __init__(self, _populationsize=100, _tournaments=5, _elitismrate=0.1, _maxgenerations=2000,
                 _mutationrate=range(1, 4), _clonelimit=30, _useclonelimit=True):
        self.population_size = _populationsize
        self.tournaments = _tournaments
        self.elitism_rate = _elitismrate
        self.max_generations = _maxgenerations
        self.mutation_rate = _mutationrate
        self.clone_limit = _clonelimit
        self.use_clone_limit = _useclonelimit

        self.elite_amount = int(self.population_size * self.elitism_rate)

    def fitness(self, _chromosome):
        """
        Calculates the travel distance for a chromosome.
        :param _chromosome: chromosome to get the travel distance
        :return: travel_distance
        """

        return sum((global_nodes_dict[_chromosome[gene - 1]][_chromosome[gene]] for gene in range(1, len(_chromosome))))

    def mutation(self, _chromosome):
        """
        Probability to mutate a chromosome to make it hopefully better...
        Details:
            - Generate a random number, if the number is in the range of the probability of mutation then it mutates.
            - The mutation is done by swapping the two half of the chromosome.
        :param _chromosome: chromosome to try to mutate
        :return: _chromosome mutated or not
        """

        probability = random.randint(1, 100)
        if probability in self.mutation_rate:
            parts = sorted(random.sample(list(range(1, len(_chromosome))), 2))
            _chromosome[parts[0]], _chromosome[parts[1]] = _chromosome[parts[1]], _chromosome[parts[0]]

        return tuple(_chromosome)

    def selection_tournament(self, _population):
        """
        Select a random number of random chromosomes from the population.
        Sorted them and make a couple out of the two best.
        :param _population: population of chromosomes
        :return: best couple
        """

        winners = random.sample(list(_population.items()), self.tournaments)
        sorted_winners = sorted(winners, key=lambda t: t[1])
        return sorted_winners[0][0], sorted_winners[1][0]

    def selection_roulette(self, chromosomes, fitnesses, targetNbChromosome):
        """
        Uses the roulette implementation of doctor Maboule
        :param chromosomes:
        :param fitnesses:
        :param targetNbChromosome:
        :return:
        """

        doctor = drMaboule.DrMaboule(["[v0(0;0)"])
        return doctor.roulette(self, chromosomes, fitnesses, targetNbChromosome)

    def crossover(self, _couple):
        """
        Makes a transgenic banana out of a couple, if you know what I mean...
        Details:
            - We define the main chromosome randomly, then we take the first half of its genes.
            - Then we add the genes of the second chromosome to the baby banana but only if they are not present yet.
        :param _couple: list of two chromosomes
        :return: transgenic_banana
        """

        couple = list(_couple)
        random.shuffle(couple)
        parts = sorted(random.sample(list(range(0, len(couple[0]))), 2))
        half = couple[0][parts[0]:parts[1]]

        transgenic_banana = [None] * len(couple[0])
        transgenic_banana[parts[0]:parts[1]] = half

        pointer = 0
        for index, item in enumerate(transgenic_banana):
            if not item:
                gene = couple[1][pointer]
                while gene in half:
                    pointer += 1
                    gene = couple[1][pointer]

                transgenic_banana[index] = couple[1][pointer]
                pointer += 1

        return transgenic_banana


def bird_distance(node1, node2):
    return int(math.sqrt(math.pow((node2[0] - node1[0]), 2) + pow((node2[1] - node1[1]), 2)))


def data_parser(file=None):
    if file is None:
        return -1

    data_dict = {}
    nodes_dict = {}
    data_file = open(file, 'r')

    for line in data_file:
        values = line.split()
        # For the values structure: v0 1 2
        nodes_dict[int(values[0][1:]) + 1] = (int(values[1]), int(values[2]))

    for node in list(nodes_dict.keys()):
        distances_dict = {}
        for next_node in nodes_dict:
            if next_node != node:
                distances_dict[next_node] = bird_distance(nodes_dict[node], nodes_dict[next_node])
            else:
                distances_dict[next_node] = 0

        data_dict[node] = distances_dict

    return data_dict


def create_population():
    """
    Creates the initial population. The origines of the bananity...
    Details:
        - Creates global_TransgenicBanana.populationSize chromosomes
        - For each new chromosome choose a random unique position from the position_possibilities_list
            - Calculate the distances and append them to the fitness_list
            - Then append the chromosome to the population_list
        - Return the population freshly made of chromosomes with random positions for genes
    """

    population_list = []
    fitness_list = []
    position_possibilities_list = tuple(range(2, len(global_nodes_dict) + 1))

    for individualChromosome in range(0, global_TransgenicBanana.population_size):

        chromosome = []
        possible = list(position_possibilities_list)

        while len(possible) != 0:
            selected = random.choice(possible)
            del possible[possible.index(selected)]
            chromosome.append(selected)

        chromosome.insert(0, 1)
        distance = global_TransgenicBanana.fitness(chromosome)

        fitness_list.append(distance)
        population_list.append(tuple(chromosome))

    population = dict(zip(population_list, fitness_list))
    population = OrderedDict(sorted(population.items(), key=lambda t: t[1]))

    return population


def darwinism(population):
    """
    Here we go, the world need a strong banana for the leadership. Everybody knows that the best are mutants!
    Generation after generation, the one shall raise.
    Details:
        - Based on the number of generation for each
            - Do the elitism (why not?) the best is the king
            - Check if previous king is a clone of the current king, if the clone limit is passed, we have the one
            - If the limit is not passed, add the other elites with king to the noble population
            - Then do the evolution
                - Selection (tournament)
                - Crossover (breed)
                - Mutation (the world rulers)
                - Population Replacement (Darwin Awards)
            - Calculate the fitness of the new population
            - And sort the new population
    :param population: initial population of bananas
    :return: best transgenic banana
    """

    best_transgenic_banana = list(population.items())[0]
    clone_counter = 0

    for generation in range(0, global_TransgenicBanana.max_generations):
        noble_population_list = []

        elite = list(population.keys())[:global_TransgenicBanana.elite_amount]
        current_banana_king = list(population.items())[0]

        if current_banana_king[1] == best_transgenic_banana[1]:
            clone_counter += 1
        elif current_banana_king[1] < best_transgenic_banana[1]:
            clone_counter = 0
            best_transgenic_banana = current_banana_king
            del elite[elite.index(current_banana_king[0])]

        if global_TransgenicBanana.clone_limit == clone_counter and global_TransgenicBanana.use_clone_limit:
            print()
            print("Clone limit achieved :)")
            break

        noble_population_list.append(best_transgenic_banana[0])
        noble_population_list.extend(elite)

        while len(noble_population_list) != global_TransgenicBanana.population_size:
            couple = global_TransgenicBanana.selection_tournament(population)
            transgenic_banana = global_TransgenicBanana.crossover(couple)
            muted_transgenic_banana = global_TransgenicBanana.mutation(transgenic_banana)
            noble_population_list.append(muted_transgenic_banana)

        fitness_list = [global_TransgenicBanana.fitness(chromosome) for chromosome in noble_population_list]
        population = dict(zip(noble_population_list, fitness_list))
        population = OrderedDict(sorted(population.items(), key=lambda t: t[1]))

        if verbose:
            fitness_average = int(sum(list(population.values())) / len(population))
            fittest = list(population.keys())[0]
            fittest_value = population[fittest]

            print()
            print("-----------------------------")
            print("Generation: #" + str(generation))
            print("Average distance: " + str(fitness_average))
            print('Current King: ' + str(best_transgenic_banana[0]))
            print('Distance: ' + str(best_transgenic_banana[1]))
            print("Chromosome with best distance: " + str(fittest))
            print("Distance: " + str(fittest_value))
            print("-----------------------------")

    print()
    print('====>>> The King arrived <<<===')
    print('Best Transgenic Banana: ' + str(best_transgenic_banana[0]))
    print('Best Distance: ' + str(best_transgenic_banana[1]))
    return best_transgenic_banana[1]


def create_ultimate_banana(_distances_dict, _verbose=False, _useclonelimit=True):
    global verbose
    verbose = _verbose
    global global_nodes_dict
    global_nodes_dict = _distances_dict
    global global_TransgenicBanana
    global_TransgenicBanana = TransgenicBanana(_useclonelimit=_useclonelimit)
    return darwinism(create_population())


if __name__ == "__main__":
    data_filename = "pb005.txt"
    number_of_tests = 2

    nodes_distances_dict = data_parser('data/' + data_filename)
    for test in range(1, number_of_tests + 1):
        print()
        print()
        print('Test #' + str(test))
        start_time = time.perf_counter()
        create_ultimate_banana(nodes_distances_dict, True)
        print("Time Elapsed: ", time.perf_counter() - start_time)
