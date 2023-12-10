import random
import entity


def convert_to_binary(value):
    return bin(value)[2:]


def convert_to_decimal(binary_string):
    return int(binary_string, 2)


def evolution(gen1, gen2):
    offspring_genotype = selection(gen1, gen2)
    offspring_genotype = crossover(offspring_genotype, random.choice([gen1, gen2]))
    mutated_offspring_genotype = mutation(offspring_genotype)
    return mutated_offspring_genotype


def selection(gen1, gen2):
    fitness1 = convert_to_decimal(gen1['num_children']) * 2 - convert_to_decimal(gen1['smell'])
    fitness2 = convert_to_decimal(gen2['num_children']) * 2 - convert_to_decimal(gen2['smell'])
    return gen1 if fitness1 > fitness2 else gen2


def fitness(entity):
    weight_for_survival = 3.0
    weight_for_food = 2.0
    weight_for_reproduction = 1.5

    fitness = (weight_for_survival * entity.age +
               weight_for_food * entity.statistic.collected_food)
    return fitness


def mutation(genotype):
    mutation_rate = 0.1
    mutated_genotype = {}
    for key, binary_value in genotype.items():
        if random.random() < mutation_rate:
            bits = list(binary_value)
            mutation_index = random.randint(0, len(bits) - 1)
            bits[mutation_index] = '0' if bits[mutation_index] == '1' else '1'
            mutated_genotype[key] = ''.join(bits)
        else:
            mutated_genotype[key] = binary_value
    return mutated_genotype


def crossover(genome1, genome2):
    child_genome = {}
    for key in genome1:
        if random.random() > 0.5:
            child_genome[key] = genome1[key]
        else:
            child_genome[key] = genome2[key]
    return child_genome
