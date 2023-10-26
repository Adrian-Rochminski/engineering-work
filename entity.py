import random


class Entity:
    def __init__(self, x, y, symbol, type, genomes):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.type = type
        self.genomes = genomes
        self.view_range = 5

    def move_up(self):
        self.y -= 1
        return 'up'

    def move_down(self):
        self.y += 1
        return 'down'

    def move_left(self):
        self.x -= 1
        return 'left'

    def move_right(self):
        self.x += 1
        return 'right'

    def get_type(self):
        return self.type

    def make_a_move(self, mapa):
        food = self.food_search(mapa)
        print(food)
        if food:
            dx, dy = min(food, key=lambda x: abs(x[0]) + abs(x[1]))
            if dx < 0 < self.x and mapa[self.y][self.x - 1] == '.':
                return self.move_left()
            elif dx > 0 and self.x < len(mapa[0]) - 1 and mapa[self.y][self.x + 1] == '.':
                return self.move_right()
            elif dy < 0 < self.y and mapa[self.y - 1][self.x] == '.':
                return self.move_up()
            elif dy > 0 and self.y < len(mapa) - 1 and mapa[self.y + 1][self.x] == '.':
                return self.move_down()
        else:
            possible_moves = []
            if self.y > 0 and mapa[self.y - 1][self.x] == '.':
                possible_moves.append('up')
            if self.y < len(mapa) - 1 and mapa[self.y + 1][self.x] == '.':
                possible_moves.append('down')
            if self.x > 0 and mapa[self.y][self.x - 1] == '.':
                possible_moves.append('left')
            if self.x < len(mapa[0]) - 1 and mapa[self.y][self.x + 1] == '.':
                possible_moves.append('right')
            if possible_moves:
                random_action = random.choice(possible_moves)
                return getattr(self, f'move_{random_action}')()

    def food_search(self, map):
        return list(filter(lambda pos: map[pos[0]][pos[1]] == 'P',
                           [(self.x + dx, self.y + dy) for dx in range(-self.view_range, self.view_range + 1) for dy in
                            range(-self.view_range, self.view_range + 1)
                            if 0 <= self.x + dx < len(map) and 0 <= self.y + dy < len(map[0])]))
