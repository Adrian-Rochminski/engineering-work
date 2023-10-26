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
    number_of_plants = config['plant_population']
    herbivores = int(number_of_population * herbivores_percent)
    carnivores = int(number_of_population * carnivores_percent)

    return number_of_population, herbivores, carnivores, number_of_plants


def generate_population():
    number_of_population, herbivores, carnivores, number_of_plants = read_conf()
    positions = [(x, y) for x in range(100) for y in range(100)]
    random.shuffle(positions)

    def create_entity(symbol, entity_type, genomes):
        x, y = positions.pop()
        return Entity(x, y, symbol, entity_type, genomes)

    population = [create_entity('H', 'herbivore', generate_genomes()) for _ in range(herbivores)]
    population.extend(create_entity('C', 'carnivore', generate_genomes()) for _ in range(carnivores))

    plants = [create_entity('P', 'plant', []) for _ in range(number_of_plants)]

    return population, plants


def generate_genomes():
    genoms = [random.random() for _ in range(10)]
    return genoms
