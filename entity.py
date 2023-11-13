import random
import genetic_algorithms as ga
import entity_performance

def find_entity_by_position(x, y, another_entities):
    for entity in another_entities:
        if entity.x == x and entity.y == y:
            return entity
    return None


class Entity:

    def __init__(self, x, y):
        self.resting_threshold = 0
        self.rest = False
        self.max_stamina = 0
        self.x = x
        self.y = y
        self.age = 1
        self.generation = 1
        self.max_age = 0
        self.min_reproductive_age = 0
        self.max_reproductive_age = 0
        self.symbol = ""
        self.food = 1
        self.required_food = 0
        self.type = ""
        self.genomes = {}
        self.view_range = 0
        self.smell = 0
        self.stamina = 0
        self.full_belly = 0
        self.num_children = 0
        self.weight = 0
        self.moves = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0),
            'up-left': (-1, -1),
            'up-right': (1, -1),
            'down-left': (-1, 1),
            'down-right': (1, 1),
            'stay': (0, 0)
        }
        self.relations = {
            'P': '-',
            'C': 'H',
            'H': 'P'
        }
        self.statuses = {
            'death': None,
            'death_from_old_age': None,
            'reproduce': None,
            'not_reproductive': None,
            'exhausted': None,
            'full_belly': None,
            'resting': None
        }
        self.statistic = entity_performance.Stats()

    def update_statistic(self, food, tick, children, food_processed, death_cause, survived_till_end):
        self.statistic.death_cause = death_cause
        self.statistic.children += children
        self.statistic.food_processed += food_processed
        self.statistic.survived_till_end = survived_till_end
        self.statistic.collected_food += food
        self.statistic.age_survived += tick

    def update_fields(self, config_data, genomes):
        self.max_age = config_data.get('max_age', self.max_age)
        self.min_reproductive_age = config_data.get('min_reproductive_age', self.min_reproductive_age)
        self.max_reproductive_age = config_data.get('max_reproductive_age', self.max_reproductive_age)
        self.symbol = config_data.get('symbol', self.symbol)
        self.required_food = config_data.get('required_food', self.required_food)
        self.type = config_data.get('type', self.type)
        self.genomes = genomes
        self.view_range = config_data.get('view_range', self.view_range)
        self.smell = config_data.get('smell', self.smell)
        self.stamina = config_data.get('stamina', self.stamina)
        self.full_belly = config_data.get('full_belly', self.full_belly)
        self.num_children = config_data.get('num_children', self.num_children)
        self.max_stamina = config_data.get('max_stamina', self.max_stamina)
        self.resting_threshold = config_data.get('resting_threshold', self.resting_threshold)

    def get_type(self):
        return self.type

    def check_status(self):
        if self.age >= self.max_age:
            return 'death_from_old_age'
        if self.stamina == 0:
            self.rest = True
            return 'exhausted'
        if self.rest:
            return 'resting'
        if self.age < self.min_reproductive_age or self.age > self.max_reproductive_age:
            return 'not_reproductive'
        return None

    def is_move_possible(self, dx, dy, mapa):
        new_x = self.x + dx if 0 <= self.x + dx < len(mapa[0]) else self.x
        new_y = self.y + dy if 0 <= self.y + dy < len(mapa) else self.y
        new_symbol = mapa[new_y][new_x]
        return new_symbol == '.' or new_symbol == self.relations[self.symbol]

    def entity_search(self, map, entity_type):
        if self.food >= self.required_food:
            entity_positions = [(self.x + dx, self.y + dy) for dx in
                                range(-self.smell, self.smell + 1) for dy in
                                range(-self.smell, self.smell + 1)
                                if 0 <= self.x + dx < len(map[0]) and 0 <= self.y + dy < len(map) and
                                map[self.y + dy][self.x + dx] == entity_type]
        else:
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

    def decide_action(self, map, another_entities):
        status = self.check_status()
        print("ssssssssssssssssssssssssssssssssssssssssssss")
        print(status)
        if status and 'death_from_old_age' in status:
            return None, 'death_from_old_age'
        if status and ('exhausted' in status or 'resting' in status):
            self.rest_entity()
            return 'stay', None
        if self.is_ready_to_reproduce():
            mate_position = self.find_nearest_mate(map)
            if mate_position:
                direction_to_mate = self.get_direction_to_entity(mate_position)
                distance_to_mate = abs(mate_position[0] - self.x) + abs(mate_position[1] - self.y)
                if distance_to_mate == 1:
                    offspring = self.reproduce(map, another_entities)
                    if offspring:
                        return offspring, 'reproduce'
                return direction_to_mate, None
        food_type = self.relations[self.symbol]
        enemy_types = [k for k, v in self.relations.items() if v == self.symbol]

        food = self.entity_search(map, food_type)
        enemies = [self.entity_search(map, enemy_type) for enemy_type in enemy_types if
                   self.entity_search(map, enemy_type)]
        print("##############")
        print(self.type)
        print(food)
        print(enemies)
        if food:
            print(self.get_direction_to_entity(food[1]))
            # print("@" + (enemies) + "@")
            print("##############")
            self.decrement_stamina()
            if not enemies or food[0] < min(enemy[0] for enemy in enemies):
                return self.get_direction_to_entity(food[1]), None
        elif enemies:
            self.decrement_stamina()
            return self.get_opposite_direction(min(enemies, key=lambda x: x[0])[1]), None
        self.rest_entity()
        return self.random_move(map), None

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

    def make_a_move(self, mapa, another_entities):
        action = self.decide_action(mapa, another_entities)

        if action:
            return action
        else:
            possible_moves = [move for move in self.moves.keys() if self.is_move_possible(*self.moves[move], mapa)]
            if possible_moves:
                return random.choice(possible_moves)

    def is_ready_to_reproduce(self):
        return (self.min_reproductive_age <= self.age <= self.max_reproductive_age) and \
            self.food >= self.required_food

    def find_nearest_mate(self, map):
        same_type_entities = self.entity_search(map, self.symbol)
        if same_type_entities:
            return same_type_entities[1]
        return None

    def get_available_neighbour_positions(self, map):
        positions = []
        for dx, dy in self.moves.values():
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < len(map[0]) and 0 <= new_y < len(map) and map[new_y][new_x] == '.':
                positions.append((new_x, new_y))
        return positions

    def is_neighbour_with_same_type(self, map):
        for dx, dy in self.moves.values():
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < len(map[0]) and 0 <= new_y < len(map) and map[new_y][new_x] == self.symbol:
                return True, (new_x, new_y)
        return False, None

    def reproduce(self, map, another_entities):
        neighbour_exist, position = self.is_neighbour_with_same_type(map)
        if neighbour_exist:
            neighbour_entity = find_entity_by_position(position[0], position[1], another_entities)
            available_positions = self.get_available_neighbour_positions(map)
            offspring_list = []
            for _ in range(min(self.num_children, len(available_positions))):
                new_x, new_y = random.choice(available_positions)
                available_positions.remove((new_x, new_y))
                offspring = self.create_child(new_x, new_y, neighbour_entity)
                offspring_list.append(offspring)
            self.food -= self.required_food
            self.full_belly = 0
            return offspring_list
        return None

    def update_entity_with_genomes(self, entity, genomes):
        for key, value in genomes.items():
            if hasattr(entity, key):
                value = value.replace('b', '')
                numeric_value = int(value, 2)
                setattr(entity, key, numeric_value)
        return entity

    def create_child(self, x, y, neighbour_entity):
        entity = Entity(x, y)
        new_children_genomes = ga.evolution(self.genomes, neighbour_entity.genomes)
        entity = self.update_entity_with_genomes(entity, new_children_genomes)
        entity.genomes = new_children_genomes
        entity.symbol = self.symbol
        entity.type = self.type
        entity.generation = self.generation + 1
        return entity

    def decrement_full_belly(self):
        if self.full_belly > 0:
            self.full_belly -= 1

    def decrement_stamina(self):
        if self.stamina > 0:
            self.stamina -= 1

    def rest_entity(self):
        if self.stamina < self.max_stamina:
            self.stamina += 1
        if self.stamina >= self.resting_threshold:
            self.rest = False

    def is_hungry(self):
        return self.food < self.required_food and self.full_belly == 0
