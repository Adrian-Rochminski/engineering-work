import csv
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
import sys

results = "Results"


def save_to_csv(distribution):
    filename = f"Population_distribution_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"
    filepath = f"Results/{filename}"

    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Game Tick", "Herbivores", "Carnivores", "Plants"])

        for tick, (herbivores, carnivores, plants) in enumerate(distribution, 1):
            writer.writerow([tick, herbivores, carnivores, plants])

    return filepath


def plot_from_csv(filepath):
    with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        ticks = []
        herbivores_data = []
        carnivores_data = []
        plants_data = []

        for row in reader:
            ticks.append(int(row[0]))
            herbivores_data.append(int(row[1]))
            carnivores_data.append(int(row[2]))
            plants_data.append(int(row[3]))

    plt.plot(ticks, herbivores_data, label='Herbivores')
    plt.plot(ticks, carnivores_data, label='Carnivores')
    plt.plot(ticks, plants_data, label='Plants')

    plt.title("Population Distribution Over Time")
    plt.xlabel("Game Tick")
    plt.ylabel("Population")
    plt.legend()
    plt.show()


def save_generation_data_to_csv(entities):
    filename = f"Generation_distribution_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"
    filepath = f"Results/{filename}"

    generation_counts = Counter(entity.generation for entity in entities)
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        generations = range(1, max(generation_counts.keys()) + 1)
        writer.writerow(['Generation'] + list(generations))
        writer.writerow(['Count'] + [generation_counts[gen] for gen in generations])

    return filepath


def plot_generation_data(filepath):
    with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        data = next(reader)

        generations = header[1:]
        counts = [int(count) for count in data[1:]]

        plt.bar(generations, counts, color='skyblue')

        plt.title("Entity Generation Distribution")
        plt.xlabel("Generation")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    plot_from_csv("Results\Population_distribution_2023-12-11.csv")
    plot_generation_data("Results/Generation_distribution_2023-12-11_15-49.csv")