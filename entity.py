class Entity:
    def __init__(self, x, y, symbol, type, genomes):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.type = type
        self.genomes = genomes

    def move_up(self):
        self.y -= 1

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1