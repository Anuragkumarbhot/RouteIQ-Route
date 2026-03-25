LARGE_NUMBER = 999_999


def nearest_neighbor(cities: list[str], distance_map: dict, start: str = None) -> dict:
    """
    Nearest Neighbor heuristic for TSP.

    Strategy:
        From the current city, always go to the closest unvisited city next.
        Repeat until all cities visited, then return to start.

    Complexity: O(n²) — handles 50+ cities easily.

    Note:
        This is a heuristic — it finds a GOOD route, not always the perfect one.
        For 3–10 cities, brute force gives the guaranteed optimal answer.
        For 11–50 cities, nearest neighbor gives a fast, practical answer.

    Args:
        cities:       List of city names to visit.
        distance_map: frozenset-keyed distance dictionary (from distance_loader).
        start:        Starting city. Defaults to cities[0].

    Returns:
        {
            "best_route":     ("Mumbai", "Pune", "Nashik"),
            "total_distance": 530,
            "all_routes":     [],          # NN doesn't enumerate all routes
            "algorithm":      "nearest_neighbor",
            "note":           "Heuristic — good route, not guaranteed optimal."
        }
    """
    if len(cities) < 2:
        raise ValueError("Need at least 2 cities.")

    start_city  = start or cities[0]
    unvisited   = [c for c in cities if c != start_city]
    route       = [start_city]
    total_dist  = 0
    current     = start_city

    while unvisited:
        # Find the nearest unvisited city from current position
        nearest      = None
        nearest_dist = float("inf")

        for city in unvisited:
            key  = frozenset({current, city})
            dist = distance_map.get(key, LARGE_NUMBER)
            if dist < nearest_dist:
                nearest_dist = dist
                nearest      = city

        # Move to nearest city
        route.append(nearest)
        total_dist += nearest_dist
        unvisited.remove(nearest)
        current = nearest

    # Return to start city (close the loop)
    return_key   = frozenset({current, start_city})
    return_dist  = distance_map.get(return_key, LARGE_NUMBER)
    total_dist  += return_dist

    return {
        "best_route":     tuple(route),
        "total_distance": total_dist,
        "all_routes":     [],   # NN builds one route, not all permutations
        "algorithm":      "nearest_neighbor",
        "note":           "Heuristic result — good route, not guaranteed optimal.",
    }


def nearest_neighbor_multi_start(cities: list[str], distance_map: dict) -> dict:
    """
    Run Nearest Neighbor from EVERY city as the start point.
    Pick the best result across all starting points.

    This significantly improves solution quality at still O(n³) —
    still fast for up to 50 cities, much better than single-start NN.
    """
    best_result = None

    for start_city in cities:
        result = nearest_neighbor(cities, distance_map, start=start_city)
        if best_result is None or result["total_distance"] < best_result["total_distance"]:
            best_result = result

    best_result["algorithm"] = "nearest_neighbor_multi_start"
    best_result["note"] = (
        f"Best of {len(cities)} starting points — "
        "good route, not guaranteed optimal."
    )
    return best_result
  
