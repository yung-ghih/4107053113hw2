import numpy as np


def generate_random_input(n_points):

    coordinates = np.random.randint(30, size=(n_points, 2))   # generate n_points coordinate range from 0 to 30
    distances_array = np.array([[np.linalg.norm(coordinates[i] - coordinates[j])
                                 for i in range(n_points)]
                                for j in range(n_points)])

    return coordinates, distances_array

