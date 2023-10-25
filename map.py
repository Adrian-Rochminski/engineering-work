import pygame
import random
from entity import Entity
import matplotlib.pyplot as plt


class Map:
    def __init__(self, width, height, entities):
        self.width = width
        self.height = height
        self.grid = [['.' for _ in range(width)] for _ in range(height)]
        self.entities = entities
        self.entity_distribution = []

    def add_entity(self, entity):
        self.entities.append(entity)
        self.grid[entity.y][entity.x] = entity.symbol

    def update(self):
        for entity in self.entities:
            self.grid[entity.y][entity.x] = '.'

            direction = random.choice(['up', 'down', 'left', 'right'])
            if direction == 'up' and entity.y > 0 and self.grid[entity.y - 1][entity.x] == '.':
                entity.move_up()
            elif direction == 'down' and entity.y < self.height - 1 and self.grid[entity.y + 1][entity.x] == '.':
                entity.move_down()
            elif direction == 'left' and entity.x > 0 and self.grid[entity.y][entity.x - 1] == '.':
                entity.move_left()
            elif direction == 'right' and entity.x < self.width - 1 and self.grid[entity.y][entity.x + 1] == '.':
                entity.move_right()

            self.grid[entity.y][entity.x] = entity.symbol

        herbivores = sum((e.get_type() == 'herbivore') for e in self.entities)
        carnivores = sum((e.get_type() == 'carnivore') for e in self.entities)
        self.entity_distribution.append((herbivores, carnivores))

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

    def draw_button(self, win, button_pos, button_size):
        button_color = (200, 200, 200)
        button_text_color = (0, 0, 0)

        button_font = pygame.font.Font(None, button_size[1] // 2)

        pygame.draw.rect(win, button_color, pygame.Rect(button_pos, button_size))

        button_text = button_font.render("instances", True, button_text_color)

        win.blit(button_text, (button_pos[0] + 10, button_pos[1] + 10))

    def display(self):
        pygame.init()

        window_width = 1000
        window_height = 500
        map_width = window_width // 2
        map_height = window_height

        win = pygame.display.set_mode((window_width, window_height))

        run = True
        while run:
            pygame.time.delay(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if map_width + 20 <= x <= map_width + 20 + button_size[0] and font_size * 5 <= y <= font_size * 5 + \
                            button_size[1]:
                        plt.plot(self.entity_distribution)
                        plt.legend(['Herbivores', 'Carnivores'])
                        plt.show()

            self.update()

            win.fill((0, 0, 0))

            pygame.draw.rect(win, (255, 255, 255), (0, 0, map_width, map_height), 1)

            self.draw_grid(win, map_width, map_height)

            font_size = window_height // 20

            self.draw_text(win, font_size, map_width)

            button_pos = (map_width + 20, font_size * 5)
            button_size = (map_width - 40, font_size * 2)

            self.draw_button(win, button_pos, button_size)

            pygame.display.update()

        pygame.quit()
