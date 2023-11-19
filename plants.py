import random
import numpy as np


class Plants:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.symbol = 'P'
        self.type = 'plants'
        self.biomass = 10
        self.age = 1
        self.nutrients_level = 0
        self.number_of_seeds = 0
        self.chance_of_seed_surviving = 10
        self.seeds_range = 0
        self.growth_rate = 0
        self.water_content = 0
        self.reproduction_frequency = 10
        self.generation = 1
        self.genomes = {}

    def grow(self, map, time):

        self.age += 1
        try:
            if time % self.reproduction_frequency == 0:
                return self.reproduce(map)
            else:
                self.photosynthesize(0)
                self.absorb_food(0, 0)
                return None
        except Exception:
            return None

    def photosynthesize(self, light_intensity):
        photosynthesis_rate = 0.1
        self.biomass += photosynthesis_rate * light_intensity

    def absorb_food(self, available_nutrients, available_water):
        nutrient_absorption_rate = 0.05
        water_absorption_rate = 0.03

        self.biomass += nutrient_absorption_rate * available_nutrients
        self.water_content += water_absorption_rate * available_water

    def fitness(self):
        return self.biomass + self.nutrients_level - self.age

    def init_from_json(self, json_data):
        fields_to_skip = ['type']
        for key, value in json_data.items():
            if key not in fields_to_skip and hasattr(self, key):
                setattr(self, key, value)
            if isinstance(value, (int, float)):
                bit_representation = format(value, 'b')
                self.genomes[key] = bit_representation
            elif isinstance(value, str):
                self.genomes[key] = ''.join([format(ord(char), 'b') for char in value])

    def assign_values_from_genomes(self):
        for key, value in self.genomes.items():
            if hasattr(self, key):
                if isinstance(value, str):
                    try:
                        decimal_value = int(value, 2)
                        setattr(self, key, decimal_value)
                    except ValueError:
                        return None

    def generate_random_positions(self, map, num_positions):
        map_array = np.array([list(row) for row in map])
        map_array = np.where(map_array == '.', 0, 1)

        start_x = max(0, self.x - self.seeds_range)
        end_x = min(map_array.shape[0], self.x + self.seeds_range + 1)
        start_y = max(0, self.y - self.seeds_range)
        end_y = min(map_array.shape[1], self.y + self.seeds_range + 1)

        possible_positions = []
        for i in range(start_x, end_x):
            for j in range(start_y, end_y):
                if map_array[j, i] == 0:
                    possible_positions.append((i, j))

        if len(possible_positions) < num_positions:
            return None

        chosen_indices = np.random.choice(len(possible_positions), num_positions, replace=False)
        random_positions = [possible_positions[i] for i in chosen_indices]
        return random_positions

    def reproduce(self, map):
        new_plants = []
        number_of_new_plants = round(self.number_of_seeds * (self.chance_of_seed_surviving / 100))
        available_positions = self.generate_random_positions(map, number_of_new_plants)
        if available_positions:
            for _, position in zip(range(number_of_new_plants), available_positions):
                new_genomes = self.mutate_genomes()
                new_plant = Plants(position[0], position[1])
                new_plant.genomes = new_genomes
                new_plant.assign_values_from_genomes()
                new_plants.append(new_plant)

            return new_plants
        return None

    def mutate_genomes(self):
        mutation_rate = 0.01
        new_genomes = {}
        for key, value in self.genomes.items():
            new_genomes[key] = ''.join(
                [self.mutate_gene(gene) if random.random() < mutation_rate else gene for gene in value])
        return new_genomes

    def mutate_gene(self, gene):
        return '1' if gene == '0' else '0'
