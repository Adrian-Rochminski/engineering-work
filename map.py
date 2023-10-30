import pygame
import random
from entity import Entity
import matplotlib.pyplot as plt


class Map:
    def __init__(self, width, height, entities, plants):
        self.width = width
        self.height = height
        self.grid = [['.' for _ in range(width)] for _ in range(height)]
        self.entities = entities
        self.entity_distribution = []
        self.plants = plants
        self.game_ticks = 0
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

    def add_entity(self, entity):
        self.entities.append(entity)
        self.grid[entity.y][entity.x] = entity.symbol

    def update(self):
        for entity in self.entities:
            self.grid[entity.y][entity.x] = '.'
            direction = entity.make_a_move(self.grid)
            print(direction)
            dx, dy = self.moves[direction]

            new_x = entity.x + dx
            new_y = entity.y + dy

            if (0 <= new_x < len(self.grid[0]) and
                    0 <= new_y < len(self.grid)):
                entity.x = new_x
                entity.y = new_y

            if entity.get_type() == 'herbivore' and any(
                    plant.x == entity.x and plant.y == entity.y for plant in self.plants):
                self.plants = list(filter(lambda plant: plant.x != entity.x or plant.y != entity.y, self.plants))
                self.grid[entity.y][entity.x] = '.'
                entity.food += 1

            print(str(entity.y) + " " + str(entity.x))
            self.grid[entity.y][entity.x] = entity.symbol

        entity_types = [e.get_type() for e in self.entities]
        herbivores = entity_types.count('herbivore')
        carnivores = entity_types.count('carnivore')
        self.entity_distribution.append((herbivores, carnivores, len(self.plants)))
        self.game_ticks += 1

    def draw_grid(self, win, map_width, map_height):
        for i in range(self.height):
            for j in range(self.width):
                color = (0, 0, 0)
                if self.grid[i][j] != '.':
                    if self.grid[i][j] == 'C':
                        color = (255, 0, 0)
                    elif self.grid[i][j] == 'H':
                        color = (0, 0, 255)
                    elif self.grid[i][j] == 'P':
                        color = (0, 255, 0)

                pygame.draw.rect(win, color,
                                 (j * map_width / self.width,
                                  i * map_height / self.height,
                                  map_width / self.width,
                                  map_height / self.height))

    def draw_text(self, win, font_size, map_width):
        font = pygame.font.Font(None, font_size)

        text = font.render('Number of objects: ' + str(len(self.entities)), True, (255, 255, 255))
        win.blit(text, (map_width + 20, font_size))

        text = font.render('Herbivores: ' + str(sum((e.get_type() == 'herbivore') for e in self.entities)), True,
                           (255, 255, 255))
        win.blit(text, (map_width + 20, font_size * 2))

        text = font.render('Carnivores: ' + str(sum((e.get_type() == 'carnivore') for e in self.entities)), True,
                           (255, 255, 255))
        win.blit(text, (map_width + 20, font_size * 3))

        text = font.render('Time: ' + str(pygame.time.get_ticks() // 1000), True,
                           (255, 255, 255))
        win.blit(text, (map_width + 20, font_size * 4))
        text = font.render('Game Ticks: ' + str(self.game_ticks), True,
                           (255, 255, 255))
        win.blit(text, (map_width + 20, font_size * 5))

        text = font.render('Plants: ' + str(len(self.plants)), True, (255, 255, 255))
        win.blit(text, (map_width + 20, font_size * 6))

    def draw_plants(self):
        for plant in self.plants:
            self.grid[plant.y][plant.x] = plant.symbol

    def draw_buttons(self, win, button_pos, button_size):
        button_color = (200, 200, 200)
        button_text_color = (0, 0, 0)

        button_font = pygame.font.Font(None, button_size[1] // 2)

        pygame.draw.rect(win, button_color, pygame.Rect(button_pos, button_size))

        button_text = button_font.render("instances", True, button_text_color)

        win.blit(button_text, (button_pos[0] + 10, button_pos[1] + 10))
        second_button_pos = (
            button_pos[0], button_pos[1] + button_size[1] + 10)
        pygame.draw.rect(win, button_color, pygame.Rect(second_button_pos, button_size))
        second_button_text = button_font.render("Check entities", True, button_text_color)
        win.blit(second_button_text, (second_button_pos[0] + 10, second_button_pos[1] + 10))

    def display(self):
        pygame.init()
        window_width = 1000
        window_height = 500
        map_width = window_width // 2
        map_height = window_height

        win = pygame.display.set_mode((window_width, window_height))
        self.draw_plants()
        run = True
        print(self.grid)
        while run:
            pygame.time.delay(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if map_width + 20 <= x <= map_width + 20 + button_size[0] and font_size * 7 <= y <= font_size * 7 + \
                            button_size[1]:
                        plt.plot(self.entity_distribution)
                        plt.legend(['Herbivores', 'Carnivores', 'Plants'])
                        plt.show()

            self.update()

            win.fill((0, 0, 0))

            pygame.draw.rect(win, (255, 255, 255), (0, 0, map_width, map_height), 1)

            self.draw_grid(win, map_width, map_height)

            font_size = window_height // 20

            self.draw_text(win, font_size, map_width)

            button_pos = (map_width + 20, font_size * 7)
            button_size = (map_width - 40, font_size * 2)

            self.draw_buttons(win, button_pos, button_size)

            pygame.display.update()

        pygame.quit()
