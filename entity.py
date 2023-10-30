import random


class Entity:
    def __init__(self, x, y, symbol, type, genomes):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.food = 0
        self.type = type
        self.genomes = genomes
        self.view_range = 5
        self.moves = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0),
            'up-left': (-1, -1),
            'up-right': (1, -1),
            'down-left': (-1, 1),
            'down-right': (1, 1)
        }
        self.relations = {
            'P': '-',
            'C': 'H',
            'H': 'P'
        }

    def get_type(self):
        return self.type


    def is_move_possible(self, dx, dy, mapa):
        new_x = self.x + dx if 0 <= self.x + dx < len(mapa[0]) else self.x
        new_y = self.y + dy if 0 <= self.y + dy < len(mapa) else self.y
        new_symbol = mapa[new_y][new_x]
        return new_symbol == '.' or new_symbol == self.relations[self.symbol]

    def entity_search(self, map, entity_type):
        entity_positions = [(self.x + dx, self.y + dy) for dx in
                            range(-self.view_range, self.view_range + 1) for dy in
                            range(-self.view_range, self.view_range + 1)
                            if 0 <= self.x + dx < len(map[0]) and 0 <= self.y + dy < len(map) and
                            map[self.y + dy][self.x + dx] == entity_type]

        if entity_positions:
            entity_positions.sort(key=lambda pos: abs(pos[0] - self.x) + abs(pos[1] - self.y))
            closest_entity = entity_positions[0]
            distance = abs(closest_entity[0] - self.x) + abs(closest_entity[1] - self.y)
            return distance, closest_entity
        return None

    def decide_action(self, map):
        food_type = self.relations[self.symbol]
        enemy_types = [k for k, v in self.relations.items() if v == self.symbol]

        food = self.entity_search(map, food_type)
        enemies = [self.entity_search(map, enemy_type) for enemy_type in enemy_types if
                   self.entity_search(map, enemy_type)]
        print("##############")
        if food:
            print(self.get_direction_to_entity(food[1]))
            # print("@" + (enemies) + "@")
            print("##############")
            if not enemies or food[0] < min(enemy[0] for enemy in enemies):
                return self.get_direction_to_entity(food[1])
        elif enemies:
            return self.get_opposite_direction(min(enemies, key=lambda x: x[0]))

        return self.random_move(map)

    def random_move(self, map):
        possible_moves = [move for move in self.moves.keys() if self.is_move_possible(*self.moves[move], map)]
        if possible_moves:
            return random.choice(possible_moves)
        return None

    def get_direction_to_entity(self, entity_position):
        dx = entity_position[0] - self.x
        dy = entity_position[1] - self.y
        dx = 0 if dx == 0 else (1 if dx > 0 else -1)
        dy = 0 if dy == 0 else (1 if dy > 0 else -1)
        direction = next((k for k, v in self.moves.items() if v == (dx, dy)), None)
        return direction

    def get_opposite_direction(self, entity_position):
        direction = self.get_direction_to_entity(entity_position)

        if direction == 'left':
            return 'right'
        elif direction == 'right':
            return 'left'
        elif direction == 'up':
            return 'down'
        elif direction == 'down':
            return 'up'
        elif direction == 'up-left':
            return 'down-right'
        elif direction == 'up-right':
            return 'down-left'
        elif direction == 'down-left':
            return 'up-right'
        elif direction == 'down-right':
            return 'up-left'

    def make_a_move(self, mapa):
        action = self.decide_action(mapa)

        if action:
            return action
        else:
            possible_moves = [move for move in self.moves.keys() if self.is_move_possible(*self.moves[move], mapa)]
            if possible_moves:
                return random.choice(possible_moves)