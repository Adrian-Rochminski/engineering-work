import random
from entity import Entity


# packed in function that does genetic algoithm

def evolution():
    pass


def selection():
    pass


def mutation():
    pass


def crossover(genoms1, genoms2):
    child_genotype = []
    for gene1, gene2 in zip(genoms1, genoms2):
        child_genotype.append(gene1 if random.random() < 0.5 else gene2)
    # child = Entity(self.x, self.y, self.symbol, self.type)
    # child.genotype = child_genotype
    # return child
    pass
