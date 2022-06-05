import matplotlib.pyplot as plt
import numpy as np
import math
import random
from random import shuffle

plt.clf()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point(" + str(self.x) + ", " + str(self.y) + ")"


def distance(point1, point2):
    return math.sqrt(((point2.x - point1.x) * (point2.x - point1.x)) + ((point2.y - point1.y) * (point2.y - point1.y)))


# parameter
beta = 2
alpha = 1
nr_ants = 40
nr_points = 40
nr_iterations = 100
pheromone_decay_parameter = 0.1
regel_fur_exploration = 1.0
random.seed(11)

# generate the points
points = []
for point_number in range(nr_points):
    points.append(Point(random.randint(0, 100), random.randint(0, 100)))

random.seed()

# plot the points
for point in points:
    plt.plot(point.x, point.y, marker="o", color="black")

# distances
distances_between_each_two_points = {}
for point1 in points:
    for point2 in points:
        if point1 is not point2:
            distances_between_each_two_points.update({frozenset((point1, point2)): distance(point1, point2)})

"""
for key in distances_between_each_two_points:
  l = list(key)
  print(l[0], ", ", l[1], " : ", distances_between_each_two_points[key])
"""

# pheromones dictionary initialization
pheromone = {}
for point1 in points:
    for point2 in points:
        if point1 is not point2:
            pheromone.update({(point1, point2): 1})

"""
for key in pheromone:
  l = list(key)
  print(l[0], ", ", l[1], " : ", pheromone[key])
"""


class Ant:
    def __init__(self, start):
        self.available = points.copy()
        self.available.remove(start)
        self.position = start
        self.path = [start]


# warscheilichkeit
def probability(point_i, point_j, ant):
    numerator = pow(pheromone[(point_i, point_j)], alpha) * pow(
        1 / distances_between_each_two_points[frozenset({point_i, point_j})], beta)

    denominator = 0
    for point_k in ant.available:
        if point_k is not point_i:
            denominator += pow(pheromone[(point_i, point_k)], alpha) * pow(
                1 / distances_between_each_two_points[frozenset({point_i, point_k})], beta)

    return numerator / denominator


def ameisenkolonie_tsp():
    t = 0
    while t <= nr_iterations:

        all_tours_length = 0
        for i in range(nr_ants):
            # initialisiere neue Ameise auf einem beliebigen stadt
            index = random.randint(0, nr_points - 1)
            ant = Ant(points[index])

            # die ameise geht durch nachsten n-1 stadte
            for k in range(1, nr_points):

                # choose next city from available after calculating each probability
                weights = []
                for j in range(0, len(ant.available)):
                    weights.append(probability(ant.position, ant.available[j], ant))
                next_city = random.choices(ant.available, weights)[0]

                # move the ant to the next city
                ant.position = next_city
                ant.path.append(next_city)
                ant.available.remove(next_city)

            # Print result
            if nr_iterations == t and i == nr_ants - 1:
                x = []
                y = []
                for pt in ant.path:
                    x.append(pt.x)
                    y.append(pt.y)
                x.append(ant.path[0].x)
                y.append(ant.path[0].y)
                plt.plot(np.array(x), np.array(y))
                plt.show()

            # ant path evaluation (rundkreis)
            path_distance = 0
            for city1 in ant.path:
                for city2 in ant.path:
                    if city1 is not city2:
                        path_distance += distances_between_each_two_points[frozenset((city1, city2))]
            path_distance += distances_between_each_two_points[frozenset((ant.path[len(ant.path) - 1], ant.path[0]))]
            all_tours_length += path_distance

            # increase pheromone for the path of this ant
            for idx1 in range(len(ant.path) - 1):
                pheromone.update({(ant.path[idx1], ant.path[idx1 + 1]): pheromone[(
                ant.path[idx1], ant.path[idx1 + 1])] + 100 / path_distance})
            pheromone.update({(ant.path[len(ant.path) - 1], ant.path[0]): pheromone[(
            ant.path[len(ant.path) - 1], ant.path[0])] + 100 / path_distance})

        # increment iteration
        t += 1

        # update pheromone matrix
        for key in pheromone:
            new_value = (1 - pheromone_decay_parameter) * pheromone[key] + 1 / all_tours_length
            pheromone.update({key: new_value})


ameisenkolonie_tsp()

# for key in pheromone:
# z = list(key)
# print(z[0], ", ", z[1], ", ", pheromone[key])
