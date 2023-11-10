import random
from entity import Entity


def evolution(gen1, gen2):
    offspring_genotype = selection(gen1, gen2)
    mutated_offspring_genotype = mutation(offspring_genotype)
    return mutated_offspring_genotype


def selection(gen1, gen2):
    fitness1 = gen1[9] * 2 - gen1[5]
    fitness2 = gen2[9] * 2 - gen2[5]
    if fitness1 > fitness2:
        return gen1
    else:
        return gen2


def mutation(genotype):
    mutation_rate = 0.1
    for i in range(len(genotype)):
        if random.random() < mutation_rate:
            mutation_value = random.choice([-1, 1])
            genotype[i] += mutation_value
            if genotype[i] < 0:
                genotype[i] = 0
    return genotype


def crossover(genome1, genome2):
    child_genome = []
    for i in range(len(genome1)):
        if random.random() > 0.5:
            child_genome.append(genome1[i])
        else:
            child_genome.append(genome2[i])
    return child_genome
