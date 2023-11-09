import pygame
import random
from entity import Entity
import matplotlib.pyplot as plt
import button


class Map:
    def __init__(self, width, height, entities, plants):
        self.buttons = None
        self.button_size = None
        self.width = width
        self.height = height
        self.grid = [['.' for _ in range(width)] for _ in range(height)]
        self.entities = entities
        self.entity_distribution = []
        self.plants = plants
        self.game_ticks = 0
        self.paused = False
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

            direction, status = entity.make_a_move(self.grid)
            print(direction)
            if status and 'death' in status:
                self.grid[entity.y][entity.x] = '.'
                self.entities.remove(entity)
            elif status and 'reproduce' in status:
                self.entities.append(direction)
            else:
                entity.age += 1
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
                elif entity.get_type() == 'carnivore':
                    herbivore_on_position = next(
                        (e for e in self.entities if
                         e.get_type() == 'herbivore' and e.x == entity.x and e.y == entity.y),
                        None)
                    if herbivore_on_position:
                        self.entities.remove(herbivore_on_position)
                        self.grid[entity.y][entity.x] = '.'
                        entity.food += 1

                print(str(entity.y) + " " + str(entity.x))
                self.grid[entity.y][entity.x] = entity.symbol
        self.count_important_data()

    def count_important_data(self):
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

    def show_popup_window(self, win, entity_details):
        popup_width = 1600
        popup_height = len(entity_details) * 30 + 10
        popup_x = (self.width - popup_width) / 2
        popup_y = (self.height - popup_height) / 2

        pygame.draw.rect(win, (200, 200, 200), (popup_x, popup_y, popup_width, popup_height))
        font = pygame.font.Font(None, 20)
        for i, detail in enumerate(entity_details):
            text = font.render(detail, True, (0, 0, 0))
            win.blit(text, (popup_x + 20, popup_y + 10 + i * 30))

    def draw_plants(self):
        for plant in self.plants:
            self.grid[plant.y][plant.x] = plant.symbol

    def create_buttons(self, map_width, font_size):
        self.buttons = []
        button_texts = ["Instances", "Check entities", "Pause"]
        button_actions = [self.show_plot, None, self.toggle_pause]

        y_pos = font_size * 7
        self.button_size = (map_width - 40, font_size * 2)
        for i, (text, action) in enumerate(zip(button_texts, button_actions)):
            button_pos = (map_width + 20, y_pos + (self.button_size[1] + 10) * i)
            self.buttons.append(button.Button(text, button_pos, self.button_size, action))

    def show_plot(self):
        plt.plot(self.entity_distribution)
        plt.legend(['Herbivores', 'Carnivores', 'Plants'])
        plt.show()

    def toggle_pause(self):
        self.paused = not self.paused

    def draw_buttons(self, win, font):
        for button in self.buttons:
            button.draw(win, font)

    def handle_button_click(self, x, y):
        for button in self.buttons:
            if button.was_clicked(x, y):
                if button.action:
                    button.action()
                return

    def display(self):
        pygame.init()
        window_width = 1000
        window_height = 500
        map_width = window_width // 2
        map_height = window_height
        popup_details = []
        popup_active = False
        win = pygame.display.set_mode((window_width, window_height))
        self.draw_plants()

        font_size = window_height // 20
        self.create_buttons(map_width, font_size)

        run = True
        while run:
            pygame.time.delay(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    clicked_entity_details = None
                    if 0 <= x < map_width and 0 <= y < map_height:
                        tile_x = int(x * self.width / map_width)
                        tile_y = int(y * self.height / map_height)
                        clicked_entity = next((e for e in self.entities if e.x == tile_x and e.y == tile_y), None)
                        if clicked_entity:
                            print("test")
                            popup_active = True
                            popup_details = [f"{field}: {value}" for field, value in vars(clicked_entity).items()]
                            print(popup_details)
                        else:
                            popup_active = False
                    else:
                        self.handle_button_click(x, y)
            if not self.paused:
                self.update()

            win.fill((0, 0, 0))
            pygame.draw.rect(win, (255, 255, 255), (0, 0, map_width, map_height), 1)
            self.draw_grid(win, map_width, map_height)
            self.draw_text(win, font_size, map_width)
            self.draw_buttons(win, pygame.font.Font(None, self.button_size[1] // 2))
            if popup_active:
                self.show_popup_window(win, popup_details)
            pygame.display.update()

        pygame.quit()
