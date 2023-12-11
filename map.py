import concurrent.futures
import time
import environment
import pygame
import matplotlib.pyplot as plt
import button
import data_saving_logic

class Map:
    def __init__(self, width, height, entities, plants):
        self.environment = environment.EnvironmentSimulator()
        self.buttons = None
        self.button_size = None
        self.width = width
        self.height = height
        self.grid = [['.' for _ in range(width)] for _ in range(height)]
        self.entities = entities
        self.genome_statistics = []
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
            'down-right': (1, 1),
            'stay': (0, 0)
        }
        self.environment.load_from_json()

    def add_entity(self, entity):
        self.entities.append(entity)
        self.grid[entity.y][entity.x] = entity.symbol

    def update(self):
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.update_entities), executor.submit(self.update_plants)]
            for future in concurrent.futures.as_completed(futures):
                future.result()
        elapsed_time = time.time() - start
        print(
            "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
        print(elapsed_time)
        print(
            "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
        self.count_important_data()
        self.environment.environment_change()

    def update_entities(self):
        for entity in self.entities:
            self.grid[entity.y][entity.x] = '.'
            food = children = food_processed = 0
            # think about it(for statistic)
            death_cause = ""
            direction, status = entity.make_a_move(self.grid, self.entities)
            print(direction)

            if status and 'death' in status:
                self.grid[entity.y][entity.x] = '.'
                self.entities.remove(entity)
            elif status and 'reproduce' in status:
                children += len(direction)
                self.entities.extend(direction)
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
                    food = 1
                elif entity.get_type() == 'carnivore':
                    herbivore_on_position = next(
                        (e for e in self.entities if
                         e.get_type() == 'herbivore' and e.x == entity.x and e.y == entity.y),
                        None)
                    if herbivore_on_position:
                        self.entities.remove(herbivore_on_position)
                        self.grid[entity.y][entity.x] = '.'
                        entity.food += 1
                        food = 1

                print(str(entity.y) + " " + str(entity.x))
                entity.update_statistic(food, 1, children, food_processed, "", False)
                self.grid[entity.y][entity.x] = entity.symbol
                self.store_genome_statistics(entity)

    def count_P_occurrences(self):
        count = 0
        for row in self.grid:
            for char in row:
                if char == 'P':
                    count += 1
        return count

    def update_plants(self):
        samplings = []
        for plant in self.plants:
            output = plant.grow(self.grid, self.game_ticks,self.environment)
            if output:
                for new_plant in output:
                    self.grid[new_plant.y][new_plant.x] = 'P'
                samplings.extend(output)
        self.plants.extend(samplings)

    def count_important_data(self):
        entity_types = [e.get_type() for e in self.entities]
        herbivores = entity_types.count('herbivore')
        carnivores = entity_types.count('carnivore')
        self.entity_distribution.append((herbivores, carnivores, len(self.plants)))
        self.game_ticks += 1

    def show_genome_statistics(self):
        if not self.genome_statistics:
            print("No genome statistics available.")
            return

        plt.figure()
        for key in self.genome_statistics[0].keys():
            plt.plot([tick[key] for tick in self.genome_statistics], label=key)

        plt.legend()
        plt.xlabel("Ticks")
        plt.ylabel("Average Genome Value")
        plt.title("Genome Statistics Over Time")
        plt.show()

    def store_genome_statistics(self, entity):
        if not self.entities:
            return
        total_genomes = {}
        for key, value in entity.genomes.items():
            if isinstance(value, (int, float)):
                if key not in total_genomes:
                    total_genomes[key] = 0
                total_genomes[key] += value

        if not total_genomes:
            return

        avg_genomes = {key: value / len(self.entities) for key, value in total_genomes.items()}
        self.genome_statistics.append(avg_genomes)

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
        button_texts = ["Instances", "Save Data", "Pause", "Show Genome Stats"]
        button_actions = [self.show_plot, self.save_data, self.toggle_pause, self.show_genome_statistics]

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

    def save_data(self):
        print("Data saved")
        data_saving_logic.save_to_csv(self.entity_distribution)
        data_saving_logic.save_generation_data_to_csv(self.entities)


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
