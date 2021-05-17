import time
import numpy as np
import matplotlib.pyplot as plt

def DP_TSP(distances_array):
    n = len(distances_array)
    all_points_set = set(range(n))

    # memo keys: tuple(sorted_points_in_path, last_point_in_path)
    # memo values: tuple(cost_thus_far, next_to_last_point_in_path)
    memo = {(tuple([i]), i): tuple([0, None]) for i in range(n)}
    queue = [(tuple([i]), i) for i in range(n)]

    while queue:
        prev_visited, prev_last_point = queue.pop(0)
        prev_dist, _ = memo[(prev_visited, prev_last_point)]

        to_visit = all_points_set.difference(set(prev_visited))
        for new_last_point in to_visit:
            new_visited = tuple(sorted(list(prev_visited) + [new_last_point]))
            new_dist = prev_dist + distances_array[prev_last_point][new_last_point]

            if (new_visited, new_last_point) not in memo:
                memo[(new_visited, new_last_point)] = (new_dist, prev_last_point)
                queue += [(new_visited, new_last_point)]
            else:
                if new_dist < memo[(new_visited, new_last_point)][0]:
                    memo[(new_visited, new_last_point)] = (new_dist, prev_last_point)

    optimal_path, optimal_cost = retrace_optimal_path(memo, n)

    return optimal_path, optimal_cost


def retrace_optimal_path(memo: dict, n: int) -> [[int], float]:
    points_to_retrace = tuple(range(n))

    full_path_memo = dict((k, v) for k, v in memo.items() if k[0] == points_to_retrace)
    path_key = min(full_path_memo.keys(), key=lambda x: full_path_memo[x][0])

    last_point = path_key[1]
    optimal_cost, next_to_last_point = memo[path_key]

    optimal_path = [last_point]
    points_to_retrace = tuple(sorted(set(points_to_retrace).difference({last_point})))

    while next_to_last_point is not None:
        last_point = next_to_last_point
        path_key = (points_to_retrace, last_point)
        _, next_to_last_point = memo[path_key]

        optimal_path = [last_point] + optimal_path
        points_to_retrace = tuple(sorted(set(points_to_retrace).difference({last_point})))

    return optimal_path, optimal_cost


def plot_route(coordinates, optimal_path):
    for p1, p2 in zip(optimal_path[:-1], optimal_path[1:]):
        plt.plot([coordinates[p1, 0], coordinates[p2, 0]], [coordinates[p1, 1], coordinates[p2, 1]])
    p1, p2 = optimal_path[-1], optimal_path[0]
    plt.plot([coordinates[p1, 0], coordinates[p2, 0]], [coordinates[p1, 1], coordinates[p2, 1]])


def generate_random_input(n_points):
    coordinates = np.random.randint(30, size=(n_points, 2))
    distances_array = np.array([[np.linalg.norm(coordinates[i] - coordinates[j])
                                 for i in range(n_points)]
                                for j in range(n_points)])
    return coordinates, distances_array


def INPUT_DP_TSP(coordinates, distances_array, index_plot):

    t = time.time()
    optimal_path, optimal_cost = DP_TSP(distances_array)
    runtime = (time.time() - t)     # Time in seconds
    print(f"Found optimal path in {runtime} seconds.")
    print(f"Optimal cost: {round(optimal_cost, 3)}, optimal path: {optimal_path}")

    if index_plot:
        print(coordinates)
        print(distances_array)

        plt.figure(figsize=(20, 15))

        plt.subplot(1, 2, 1)
        plt.scatter(coordinates[:, 0], coordinates[:, 1])

        plt.subplot(1, 2, 2)
        plot_route(coordinates, optimal_path)

        plt.tight_layout()
        plt.show()

    return runtime, optimal_cost, optimal_path
