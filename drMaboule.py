__author__ = 'stevevisinand'

from random import randint
import math


class DrMaboule:
    def __init__ (self, listCities) :
        self._listCities = listCities


    # nbCities is the size of each chromosome
    # nbChromosomes define how many Chromosomes you need
    def fitness(self, nbCities, nbChromosomes):

        chromosomes = [] # contain cities list
        fitnesses = []  # contain fitness for chromosomes (at same index)

        for c in range(nbChromosomes) :

            #select random path without "doublons"
            randCities = []

            fitess = 0

            while len(randCities) < nbCities :
                randIndex = randint(0, len(self._listCities)-1)
                if(self._listCities[randIndex] not in randCities):

                    #calculate fitness
                    if(len(randCities) > 0):
                        city1 =  randCities[len(randCities)-1]
                        city2 =  self._listCities[randIndex]

                        fitess += math.sqrt(pow((city2.posX - city1.posX), 2) + pow((city2.posY - city1.posY), 2))

                    #add city
                    randCities.append(self._listCities[randIndex])


            fitnesses.append(fitess)
            chromosomes.append(randCities)


        return chromosomes, fitnesses


    # multFactor define how many chromosomes you will have more !
    # 1.0 = +100%, 0.5 = + 50%, 2.0 = + 200%
    def crossing(self, chromosomes, fitnesses, multFactor):

        # number of croising necessary to get the multFactor
        nbAdd = int(len(chromosomes) * multFactor)

        for x in range(nbAdd):

            #sort chromosome 1
            chromosome_1 = chromosomes[randint(0, len(chromosomes)-1)]

            #sort chromosome 2
            chromosome_2 = chromosomes[randint(0, len(chromosomes)-1)]

            #get halfs
            sizeHalf = int(len(chromosome_1)/2)
            half_1 = chromosome_1[sizeHalf:]
            half_2 = chromosome_2[:sizeHalf]


            #ATTENTION : never visit 2 same cities in a chromosome
            while self.haveDoublonInHalf(half_1, half_2):
                chromosome_2 = chromosomes[randint(0, len(chromosomes)-1)]
                half_2 = chromosome_2[:sizeHalf]

            #crossing
            newChromosome = half_1
            newChromosome.extend(half_2)

            #calcul fitness
            fitness = 0
            city1 = newChromosome[0]
            for i in range(1, len(newChromosome)):
                city2 = newChromosome[i]

                fitness += math.sqrt(pow((city2.posX - city1.posX), 2) + pow((city2.posY - city1.posY), 2))

                city1 = city2

            #same index between fitnesses and chromosomes
            chromosomes.append(newChromosome)
            fitnesses.append(fitness)

        return chromosomes, fitnesses

    #select the bests N chromosomes (N = targetNbChromosome)
    def roulette(self, chromosomes, fitnesses, targetNbChromosome):

        totalFitness = 0
        for fit in fitnesses:
            totalFitness += fit


        newFitnesses = []
        newChromosomes = []

        for x in range(targetNbChromosome):

            value = randint(0, int(totalFitness))

            fit=0
            i = 0
            while fit<=value :
                fit += fitnesses[i]
                i+=1

            i-=1

            #remove already sorted
            newFitnesses.append(fitnesses[i])
            newChromosomes.append(chromosomes.pop(i))

            totalFitness -= fitnesses.pop(i)

        return newChromosomes, newFitnesses


    #simply exchange two city in a list
    def mutation(self, chromosomes, fitnesses, percentMutation):
        nbMutation = int(len(chromosomes) * percentMutation)

        for x in range(nbMutation):

            chromosome_index = randint(0, len(chromosomes)-1)


            city1_index = randint(0, len(chromosomes[chromosome_index])-1)
            city2_index = randint(0, len(chromosomes[chromosome_index])-1)

            tmp = chromosomes[chromosome_index][city1_index]
            chromosomes[chromosome_index][city1_index] = chromosomes[chromosome_index][city2_index]
            chromosomes[chromosome_index][city2_index] = tmp


        return chromosomes, fitnesses



    def work(self, nbIterations):

        nbChromosome = 10
        nbCitiesPerChromosome = 10
        percentMutation = 0.2

        chromosomes, fitnesses = self.fitness(nbCitiesPerChromosome, nbChromosome)

        for i in range(nbIterations):
            chromosomes, fitnesses = self.crossing(chromosomes, fitnesses, 1.0)
            chromosomes, fitnesses = self.roulette(chromosomes, fitnesses, nbChromosome)
            chromosomes, fitnesses = self.mutation(chromosomes, fitnesses, percentMutation)

        #return best
        bestIndex = -1
        for i in range(len(fitnesses)):
            if fitnesses[i] > fitnesses[bestIndex]:
                bestIndex = i

        return chromosomes[bestIndex], fitnesses[bestIndex]



    #check if it exist same cities in first half of chromosome_1 and chromosome_2
    def haveDoublonInHalf(self, half_1, half_2):
        for city in half_1:
            if(city in half_2):
                return True
        return False


