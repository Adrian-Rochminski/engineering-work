from map import Map
from Entities_generation import generate_population


def main():
    entities_population = generate_population()
    game_map = Map(100, 100, entities_population)
    game_map.display()


if __name__ == "__main__":
    main()
