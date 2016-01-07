import random
import string

GA_POPSIZE = 2048
GA_ELITRATE = 0.10  # elitism rate
GA_MUTATIONRATE = 0.25  # mutation rate
GA_TARGET = "Hello world!"
GA_CHARS = string.ascii_letters + string.digits + string.punctuation + string.whitespace


def randstr():
    return "".join([random.choice(GA_CHARS) for i in range(len(GA_TARGET))])


def fitness(value):
    return sum([abs(ord(value[j]) - ord(GA_TARGET[j])) for j in range(len(GA_TARGET))])


def mate(population, buffer):
    esize = int(GA_POPSIZE * GA_ELITRATE)
    for i in range(esize):  # Elitism
        buffer[i] = population[i]
    for i in range(esize, GA_POPSIZE):
        i1 = random.randint(0, GA_POPSIZE / 2)
        i2 = random.randint(0, GA_POPSIZE / 2)
        spos = random.randint(0, len(GA_TARGET))
        buffer[i] = population[i1][:spos] + population[i2][spos:]  # Mate
        if random.random() < GA_MUTATIONRATE:  # Mutate
            pos = random.randint(0, len(GA_TARGET) - 1)
            buffer[i] = buffer[i][:pos] + random.choice(GA_CHARS) + buffer[i][pos + 1:]


population = [randstr() for i in range(GA_POPSIZE)]
buffer = [randstr() for i in range(GA_POPSIZE)]
i = 0
while True:
    population = sorted(population, key=lambda c: fitness(c))
    print("[%03d]\tBest (%04d)\t%s" % (i, fitness(population[0]), population[0]))
    if not fitness(population[0]):  # We're done, best match found
        break
    mate(population, buffer)
    population, buffer = buffer, population
    i += 1
