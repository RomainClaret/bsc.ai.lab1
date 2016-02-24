import os, sys
import pygame
from pygame.locals import *
import time
import math
import random
from collections import OrderedDict


# if not pygame.font:
#    print('Warning, fonts disabled')
# if not pygame.mixer:
#    print('Warning, sound disabled')


#Values necessary for pygame
screen_x = 500
screen_y = 500

city_color = [10,10,200] # blue
city_radius = 3

font_color = [255,255,255] # white



def ga_solve(filename=None, gui=True, maxtime=0):
    """
    :param filename: ....txt
    :param gui: True or False #todo !
    :param maxtime: temps max
    :return: length (fitness), path (chemin de villes)
    """


    if filename == None:
        pygame.init()
        window = pygame.display.set_mode((screen_x, screen_y))
        pygame.display.set_caption('The king of bananas')
        screen = pygame.display.get_surface()

        screen.fill(0)

        collecting = True

        font = pygame.font.Font(None,30)
        cities = []

        while collecting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_RETURN:
                    collecting = False
                elif event.type == MOUSEBUTTONDOWN:
                    cities.append(pygame.mouse.get_pos())
                    screen.fill(0)
                    drawPoint(cities, screen)
                    pygame.display.flip()


        nodes_distances_dict, nodes_pos = data_screen_parser(cities)


    else:
        # Parse
        nodes_distances_dict, nodes_pos = data_parser(filename)

        screen = None
        # Show
        if gui:
            pygame.init()
            window = pygame.display.set_mode((screen_x, screen_y))
            pygame.display.set_caption('The king of bananas')
            screen = pygame.display.get_surface()

            screen.fill(0)
            drawPoint(nodes_pos.values(), screen)
            pygame.display.flip()

            event = pygame.event.wait()




    # Start !
    global verbose
    verbose = False

    global global_nodes_dict
    global_nodes_dict = nodes_distances_dict

    global global_TransgenicBanana
    global_TransgenicBanana = TransgenicBanana(maxtime)

    return darwinism(create_population(), nodes_pos, screen)


def drawPoint(positions, screen):
    font = pygame.font.Font(None,30)

    for pos in positions:
        pygame.draw.circle(screen,city_color,pos,city_radius)
    text = font.render("Nombre: %i" % len(positions), True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)



def drawChromosome(screen, transgenic_banana, nodes_pos, score):
    screen.fill(0)

    oldCityId = transgenic_banana[0]

    i=1
    while i < len(transgenic_banana):
        cityId = transgenic_banana[i]

        city1 = nodes_pos[cityId]
        city2 = nodes_pos[oldCityId]

        pygame.draw.line(screen, [240,255,0], city1, city2, 2)

        oldCityId = cityId
        i+=1

    #last line
    pygame.draw.line(screen, [240,255,0], nodes_pos[transgenic_banana[0]], nodes_pos[transgenic_banana[-1]], 2)

    font = pygame.font.Font(None,30)
    text = font.render("Score: %i" % score, True, font_color)
    textRect = text.get_rect()
    screen.blit(text, (0, 20))

    drawPoint(nodes_pos.values(), screen)
    pygame.display.flip()



def ga_solver_brute(filename, gui, maxtime, populationsize, tournaments, elitismrate, mutationrate):
    # Parse
    nodes_distances_dict, node_pos = data_parser(filename)

    # Start !
    global verbose
    verbose = False

    global global_nodes_dict
    global_nodes_dict = nodes_distances_dict

    global global_TransgenicBanana
    global_TransgenicBanana = TransgenicBanana(maxtime, _populationsize=populationsize, _tournaments=tournaments,
                                               _elitismrate=elitismrate, _mutationrate=mutationrate)

    return darwinism(create_population())


def dist(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return math.hypot(x2 - x1, y2 - y1)


class TransgenicBanana:
    def __init__(self, _maxtime, _populationsize=100, _tournaments=7, _elitismrate=0.1,
                 _maxgenerations=2000, _mutationrate=0.4, _clonelimit=30):
        self.population_size = _populationsize
        self.tournaments = _tournaments
        self.elitism_rate = _elitismrate
        self.max_generations = _maxgenerations
        self.use_max_generation = (_maxtime <= 0)
        self.mutation_rate = _mutationrate
        self.clone_limit = _clonelimit
        self.use_clone_limit = (_maxtime <= 0)
        self.maxtime = _maxtime


        self.elite_amount = int(self.population_size * self.elitism_rate)

    def fitness(self, _chromosome):
        """
        First looping the chromosome, last goes to first
        Calculates the total travel distance for a chromosome.
        :param _chromosome: chromosome to get the travel distance
        :return: travel_distance
        """

        looped_chromosome = list(_chromosome)
        looped_chromosome.append(_chromosome[0])
        _chromosome = tuple(looped_chromosome)

        return sum(
            (global_nodes_dict[_chromosome[gene]][_chromosome[gene + 1]] for gene in range(0, len(_chromosome) - 1)))

    def mutation(self, _chromosome):
        """
        Probability to mutate a chromosome to make it hopefully better...
        Details:
            - Generate a random number, if the number is in the range of the probability of mutation then it mutates.
            - The mutation is done by swapping the two half of the chromosome.
        :param _chromosome: chromosome to try to mutate
        :return: _chromosome mutated or not
        """

        probability = random.randint(1, 100) / 100
        if probability >= self.mutation_rate:
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
    # return int(math.sqrt(math.pow((node2[0] - node1[0]), 2) + pow((node2[1] - node1[1]), 2)))
    x1, y1 = node1
    x2, y2 = node2
    return math.hypot(x2 - x1, y2 - y1)

def dist_calcul(nodes_dict):
    """
    (pre)Calculate the distance between cities
    """
    data_dict = {}
    for node in list(nodes_dict.keys()):
        distances_dict = {}
        for next_node in nodes_dict:
            if next_node != node:
                distances_dict[next_node] = bird_distance(nodes_dict[node], nodes_dict[next_node])
            else:
                distances_dict[next_node] = 0

        data_dict[node] = distances_dict
    return data_dict

def data_parser(file=None):
    if file is None:
        return -1

    nodes_dict = {}
    data_file = open(file, 'r')


    for line in data_file:
        values = line.split()
        # For the values structure: v0 1 2
        nodes_dict[int(values[0][1:]) + 1] = (int(values[1]), int(values[2]))


    data_dict = dist_calcul(nodes_dict)

    return data_dict, nodes_dict #nodes_dict contain pos


def data_screen_parser(citiesPos):

    nodes_dict = {}

    i=1
    for city in citiesPos:
        # For the values structure: v0 1 2
        nodes_dict[i] = (int(city[0]), int(city[1]))
        i+=1


    data_dict = dist_calcul(nodes_dict)

    return data_dict, nodes_dict #nodes_dict contain pos



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


def darwinism(population, nodes_pos, screen=None):
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

    start = time.time()
    generation = 0

    print("global_TransgenicBanana.use_max_generation", global_TransgenicBanana.use_max_generation)
    print("generation < global_TransgenicBanana.max_generations", generation < global_TransgenicBanana.max_generations)
    print("generation < global_TransgenicBanana.max_generations and global_TransgenicBanana.use_max_generation", generation < global_TransgenicBanana.max_generations and global_TransgenicBanana.use_max_generation)

    while generation < global_TransgenicBanana.max_generations or global_TransgenicBanana.use_max_generation:

        noble_population_list = []

        elite = list(population.keys())[:global_TransgenicBanana.elite_amount]
        current_banana_king = list(population.items())[0]

        if current_banana_king[1] == best_transgenic_banana[1]:
            clone_counter += 1
        elif current_banana_king[1] < best_transgenic_banana[1]:
            clone_counter = 0
            best_transgenic_banana = current_banana_king
            del elite[elite.index(current_banana_king[0])]

        # Stop Algo
        if global_TransgenicBanana.clone_limit == clone_counter \
                and global_TransgenicBanana.use_clone_limit:
            if verbose:
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
        # print(population)

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


        if screen is not None:
            #GUI is ON
            drawChromosome(screen, best_transgenic_banana[0], nodes_pos, best_transgenic_banana[1])

        if (time.time() - start) >= global_TransgenicBanana.maxtime and not global_TransgenicBanana.use_max_generation:
            if verbose:
                print("Time finished")
            break

        generation += 1


    # convert 1 to 'v0', 2 to 'v1' ...
    best_city_path = []
    for cityNb in best_transgenic_banana[0]:
        best_city_path.append('v' + str(cityNb - 1))

    print("\n  _____ _          _  ___                          _            _ ")
    print(" |_   _| |_  ___  | |/ (_)_ _  __ _   __ _ _ _ _ _(_)_ _____ __| |")
    print("   | | | ' \/ -_) | ' <| | ' \/ _` | / _` | '_| '_| \ V / -_) _` |")
    print("   |_| |_||_\___| |_|\_\_|_||_\__, | \__,_|_| |_| |_|\_/\___\__,_|")
    print("                              |___/                               ")

    print('Best Transgenic Banana: ' + str(best_city_path))
    print('Best Distance: ' + str(best_transgenic_banana[1]))
    print('Nb generation: ' + str(generation))


    if screen is not None :
        font = pygame.font.Font(None,30)
        text = font.render("The King arrived!", True, font_color)
        screen.blit(text, (160, 10))

        textE = font.render("Press ENTER", True, font_color)
        screen.blit(textE, (180, 475))
        pygame.display.flip()

        while True:
            event = pygame.event.wait()
            if event.type == KEYDOWN: break

    return best_transgenic_banana[1], best_city_path



if __name__ == "__main__":
    # test here
    #print("\nga_solve : ", ga_solve("data/pb020.txt", True, 2))
    #print("\nga_solve : ", ga_solve(None, True))


    gui = True
    fileName = None
    maxtime = 0

    for iArg in range(1,len(sys.argv)):

        if sys.argv[iArg] == "--nogui":
            gui = False
        elif sys.argv[iArg] == "--maxtime":
            maxtime = int(sys.argv[iArg + 1])
        else:
            if sys.argv[iArg -1] != "--maxtime":
                fileName = str(sys.argv[iArg])


    print("GUI : ", gui)
    print("fileName : ", fileName)
    print("maxtime : ", maxtime)

    ga_solve(fileName, gui, maxtime)
