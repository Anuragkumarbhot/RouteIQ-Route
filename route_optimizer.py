from fastapi import APIRouter, HTTPException, Query, Request
from models.schemas import (
    OptimizeRequest, OptimizeResponse, RouteResult,
    DistanceResponse, CitiesResponse
)
from services import location_manager, route_generator, optimizer
from services.nearest_neighbor import nearest_neighbor, nearest_neighbor_multi_start
from services.distance_calculator import calculate_route_distance

router = APIRouter()

# Auto-select threshold: brute force below this, nearest neighbor above
BRUTE_FORCE_LIMIT = 10


def get_distance_map(request: Request) -> dict:
    """Pull the cached distance_map from app.state (zero disk reads)."""
    return request.app.state.distance_map


def _select_algorithm(cities: list[str], requested: str) -> str:
    """
    Decide which algorithm to actually run.

    auto         → brute_force if ≤10 cities, else nearest_neighbor_multi_start
    brute_force  → always brute force (caller must ensure ≤12 cities)
    nearest_neighbor             → single-start NN
    nearest_neighbor_multi_start → best-of-all-starts NN
    """
    if requested == "auto":
        return "brute_force" if len(cities) <= BRUTE_FORCE_LIMIT else "nearest_neighbor_multi_start"
    return requested


@router.post("/optimize", response_model=OptimizeResponse)
def optimize_route(request: OptimizeRequest, req: Request):
    """
    Find the shortest route across all provided cities, returning to start.

    Algorithms:
    - **auto** *(default)*: brute force for ≤10 cities, nearest neighbor for 11–50
    - **brute_force**: guaranteed optimal, max 12 cities
    - **nearest_neighbor**: fast heuristic, single start point
    - **nearest_neighbor_multi_start**: best-of-all-starts heuristic, best quality
    """
    try:
        distance_map = get_distance_map(req)
        location_manager.validate_cities(request.cities, distance_map)

        algo = _select_algorithm(request.cities, request.algorithm)

        # ── Brute Force ─────────────────────────────────────────────────────
        if algo == "brute_force":
            routes = route_generator.generate_routes(request.cities)
            result = optimizer.find_best_route(routes, distance_map)
            result["algorithm"]     = "brute_force"
            result["note"]          = "Guaranteed optimal result."
            routes_checked          = len(routes)
            all_routes              = [
                RouteResult(
                    route=list(r["route"]) + [r["route"][0]],
                    distance_km=r["distance"]
                )
                for r in result["all_routes"]
            ]

        # ── Nearest Neighbor (single start) ─────────────────────────────────
        elif algo == "nearest_neighbor":
            result       = nearest_neighbor(request.cities, distance_map)
            routes_checked = 1
            all_routes   = []

        # ── Nearest Neighbor (multi-start) ──────────────────────────────────
        elif algo == "nearest_neighbor_multi_start":
            result       = nearest_neighbor_multi_start(request.cities, distance_map)
            routes_checked = len(request.cities)
            all_routes   = []

        else:
            raise ValueError(f"Unknown algorithm: {algo}")

        best_loop = list(result["best_route"]) + [result["best_route"][0]]

        return OptimizeResponse(
            best_route=best_loop,
            total_distance_km=result["total_distance"],
            all_routes=all_routes,
            cities_count=len(request.cities),
            routes_checked=routes_checked,
            algorithm_used=result["algorithm"],
            note=result.get("note"),
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/cities", response_model=CitiesResponse)
def get_all_cities(req: Request):
    """Return all cities available in the distance dataset."""
    distance_map = get_distance_map(req)
    all_cities = set()
    for key in distance_map:
        all_cities.update(key)
    return CitiesResponse(cities=sorted(all_cities))


@router.get("/distance", response_model=DistanceResponse)
def get_distance(
    req: Request,
    city1: str = Query(..., description="First city name"),
    city2: str = Query(..., description="Second city name"),
):
    """Return the direct distance between two cities."""
    distance_map = get_distance_map(req)
    key = frozenset({city1.strip().title(), city2.strip().title()})
    dist = distance_map.get(key)
    if dist is None:
        raise HTTPException(
            status_code=404,
            detail=f"No distance found between '{city1}' and '{city2}'."
        )
    return DistanceResponse(
        city1=city1.strip().title(),
        city2=city2.strip().title(),
        distance_km=dist,
  )
  
