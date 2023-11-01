import json


env_file = "environment.json"


def read_env_file():
    with open(env_file, 'r') as f:
        config = json.load(f)

    number_of_population = config['number_of_population']
    herbivores_percent = config['herbivores_percent']
    carnivores_percent = config['carnivores_percent']
    number_of_plants = config['plant_population']
    herbivores = int(number_of_population * herbivores_percent)
    carnivores = int(number_of_population * carnivores_percent)

    return number_of_population, herbivores, carnivores, number_of_plants
