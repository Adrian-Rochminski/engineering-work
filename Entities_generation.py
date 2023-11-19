import random
from entity import Entity
from plants import Plants
import json

config_file = "conf_file.json"
entity_stats_h = "entity_stats_h.json"
entity_stats_c = "entity_stats_c.json"
plants_stats = "plants_stats.json"


def read_entity(file_path):
    with open(file_path, 'r') as file:
        entity_data = json.load(file)
        return entity_data


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


def convert_to_binary(json_data):
    binary_data = {}
    for key, value in json_data.items():
        if key not in ["genomes", "symbol", "type"]:
            if isinstance(value, (int, float)):
                binary_data[key] = bin(value)
    return binary_data


def generate_population():
    number_of_population, herbivores, carnivores, number_of_plants = read_conf()
    positions = [(x, y) for x in range(100) for y in range(100)]
    random.shuffle(positions)
    herbivores_stats = read_entity(entity_stats_h)
    carnivore_stats = read_entity(entity_stats_c)
    plant_stats = read_entity(plants_stats)

    def create_entity(conf):
        x, y = positions.pop()
        entity = Entity(x, y)
        entity.update_fields(conf, convert_to_binary(conf))
        return entity

    def create_plant(conf):
        x, y = positions.pop()
        plant = Plants(x, y)
        plant.init_from_json(conf)
        return plant

    population = [create_entity(herbivores_stats) for _ in range(herbivores)]
    population.extend(create_entity(carnivore_stats) for _ in range(carnivores))

    plants = [create_plant(plant_stats) for _ in range(number_of_plants)]

    return population, plants


def generate_genomes():
    genoms = [random.random() for _ in range(10)]
    return genoms
