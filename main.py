from map import Map
import Entities_generation

game_map = None


def initialize_map():
    global game_map
    entities_population, plant_population = Entities_generation.generate_population()
    game_map = Map(100, 100, entities_population, plant_population)


def main():
    initialize_map()
    game_map.display()


if __name__ == "__main__":
    main()
