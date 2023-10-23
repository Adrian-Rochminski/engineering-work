import random
from entity import Entity
import json

config_file = "conf_file.json"


def read_conf():
    with open(config_file, 'r') as f:
        config = json.load(f)

    number_of_population = config['number_of_population']
    herbivores_percent = config['herbivores_percent']
    carnivores_percent = config['carnivores_percent']

    herbivores = int(number_of_population * herbivores_percent)
    carnivores = int(number_of_population * carnivores_percent)

    return number_of_population, herbivores, carnivores


def generate_population():
    population = []
    number_of_population, herbivores, carnivores = read_conf()
    for _ in range(herbivores):
        genomes = generate_genomes()
        entity = Entity( random.randint(0,99), random.randint(0,99), 'H', 'herbivore', genomes)
        population.append(entity)

    for _ in range(carnivores):
        genomes = generate_genomes()
        entity = Entity(random.randint(0,99), random.randint(0,99), 'C', 'carnivore', genomes)
        population.append(entity)
    return population


def generate_genomes():
    genoms = [random.random() for _ in range(10)]
    return genoms
