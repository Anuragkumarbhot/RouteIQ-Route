from concurrent.futures import ProcessPoolExecutor
import os
from itertools import permutations


def calculate_route(route, distance_map):

    total = 0

    for i in range(len(route) - 1):

        city1 = route[i]

        city2 = route[i + 1]

        if (city1, city2) in distance_map:

            total += distance_map[
                (city1, city2)
            ]

        elif (city2, city1) in distance_map:

            total += distance_map[
                (city2, city1)
            ]

        else:

            return None

    last_city = route[-1]

    first_city = route[0]

    if (last_city, first_city) in distance_map:

        total += distance_map[
            (last_city, first_city)
        ]

    elif (first_city, last_city) in distance_map:

        total += distance_map[
            (first_city, last_city)
        ]

    else:

        return None

    return total


def optimize_parallel(locations, distance_map):

    routes = list(
        permutations(locations)
    )

    if len(routes) < 500:

        return optimize_single(
            routes,
            distance_map
        )

    workers = os.cpu_count()

    with ProcessPoolExecutor(
        workers
    ) as executor:

        results = executor.map(
            lambda r:
            (r, calculate_route(r, distance_map)),
            routes
        )

    best_route = None

    best_distance = float("inf")

    for route, dist in results:

        if dist and dist < best_distance:

            best_distance = dist

            best_route = route + (route[0],)

    return best_route, best_distance


def optimize_single(routes, distance_map):

    best_route = None

    best_distance = float("inf")

    for route in routes:

        dist = calculate_route(
            route,
            distance_map
        )

        if dist and dist < best_distance:

            best_distance = dist

            best_route = route + (route[0],)

    return best_route, best_distance
