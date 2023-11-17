from random import random


class Plants:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.symbol = ''
        self.type = ''
        self.biomass = ''
        self.age = 0
        self.nutrients_level = 0
        self.number_of_seeds = 0
        self.chance_of_seed_surviving = 0.4
        self.growth_rate = 0
        self.water_content = 0
        self.genomes = {}

    def grow(self):
        pass

    def photosynthesize(self):
        pass

    def absorb_food(self):
        pass

    def fitness(self):
        return self.biomass + self.nutrients_level - self.age

    def reproduce(self):
        new_plants = []
        number_of_new_plants = round(self.number_of_seeds * self.chance_of_seed_surviving)
        for _ in range(number_of_new_plants):
            new_genomes = self.mutate_genomes()
            new_plants.append(Plants(genomes=new_genomes))
        return new_plants

    def mutate_genomes(self):
        mutation_rate = 0.01
        new_genomes = {}
        for key, value in self.genomes.items():
            new_genomes[key] = ''.join(
                [self.mutate_gene(gene) if random.random() < mutation_rate else gene for gene in value])
        return new_genomes

    def mutate_gene(self, gene):
        return '1' if gene == '0' else '0'