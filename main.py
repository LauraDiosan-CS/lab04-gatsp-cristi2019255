import math

from lab_05.aco import ACO, Graph
from lab_05.plot import plot


def distance(city1: dict, city2: dict):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)


def main():
    cities = []
    points = []
    with open('harde.txt') as f:

        for line in f.readlines():
            city = line.split(" ")
            cities.append(dict(index=int(city[0]), x=int(math.floor(float(city[1]))), y=int(math.floor(float(city[2])))))
            points.append((int(math.floor(float(city[1]))), int(math.floor(float(city[2])))))
        cost_matrix = []
        rank = len(cities)
        for i in range(rank):
            row = []
            for j in range(rank):
                row.append(distance(cities[i], cities[j]))
            cost_matrix.append(row)
        aco = ACO(30, 100, 1.0, 10.0, 0.5, 10, 0, points)
        graph = Graph(cost_matrix, rank)
        path, cost = aco.solve(graph)
        print('cost: {}, path: {}'.format(cost, path))
        plot(points, path)


if __name__ == '__main__':
    main()
