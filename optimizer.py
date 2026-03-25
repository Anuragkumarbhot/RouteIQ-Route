from services.distance_calculator import calculate_route_distance


def find_best_route(routes: list[tuple], distance_map: dict) -> dict:
    """
    Evaluate all routes and return the one with the lowest total distance.

    Returns:
        {
            "best_route": ("Mumbai", "Pune", "Nashik"),
            "total_distance": 530,
            "all_routes": [{"route": ..., "distance": ...}, ...]
        }
    """
    best_route = None
    best_distance = float("inf")
    all_routes = []

    for route in routes:
        dist = calculate_route_distance(route, distance_map)
        all_routes.append({"route": route, "distance": dist})

        if dist < best_distance:
            best_distance = dist
            best_route = route

    return {
        "best_route": best_route,
        "total_distance": best_distance,
        "all_routes": all_routes,
    }
  
