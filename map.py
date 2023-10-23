import pygame
import random
from entity import Entity


class Map:
    def __init__(self, width, height,entities):
        self.width = width
        self.height = height
        self.grid = [['.' for _ in range(width)] for _ in range(height)]
        self.entities = entities

    def add_entity(self, entity):
        self.entities.append(entity)
        self.grid[entity.y][entity.x] = entity.symbol

    def update(self):
        for entity in self.entities:
            self.grid[entity.y][entity.x] = '.'

            direction = random.choice(['up', 'down', 'left', 'right'])
            if direction == 'up' and entity.y > 0:
                entity.move_up()
            elif direction == 'down' and entity.y < self.height - 1:
                entity.move_down()
            elif direction == 'left' and entity.x > 0:
                entity.move_left()
            elif direction == 'right' and entity.x < self.width - 1:
                entity.move_right()
            self.grid[entity.y][entity.x] = entity.symbol

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
            self.update()
            win.fill((0, 0, 0))
            pygame.draw.rect(win, (255, 255, 255), (0, 0, map_width, map_height), 1)
            for i in range(self.height):
                for j in range(self.width):
                    if self.grid[i][j] == '.':
                        pygame.draw.rect(win, (0, 0, 0), (
                        j * map_width / self.width, i * map_height / self.height, map_width / self.width,
                        map_height / self.height))
                    else:
                        pygame.draw.rect(win, (255, 255, 255), (
                        j * map_width / self.width, i * map_height / self.height, map_width / self.width,
                        map_height / self.height))
            font_size = window_height // 20
            font = pygame.font.Font(None, font_size)
            text = font.render('Number of objects: ' + str(len(self.entities)), True, (255, 255, 255))
            win.blit(text, (map_width + 20, font_size))

            text = font.render('Time: ' + str(pygame.time.get_ticks() // 1000), True, (255, 255, 255))
            win.blit(text, (map_width + 20, font_size * 3))

            button_color = (200, 200, 200)
            button_text_color = (0, 0, 0)
            button_pos = (map_width + 20, font_size * 5)
            button_size = (map_width - 40, font_size * 2)

            button_font = pygame.font.Font(None, font_size)

            pygame.draw.rect(win, button_color, pygame.Rect(button_pos, button_size))

            button_text = button_font.render("instances", True, button_text_color)

            win.blit(button_text, (button_pos[0] + 10, button_pos[1] + 10))

            pygame.display.update()

        pygame.quit()
