from typing import Literal
from pydantic import BaseModel, field_validator, model_validator


# ── Request Models ──────────────────────────────────────────────────────────

class OptimizeRequest(BaseModel):
    cities: list[str]
    algorithm: Literal["auto", "brute_force", "nearest_neighbor", "nearest_neighbor_multi_start"] = "auto"

    @field_validator("cities")
    @classmethod
    def validate_city_list(cls, v):
        if len(v) < 2:
            raise ValueError("Provide at least 2 cities.")
        if len(v) > 50:
            raise ValueError("Maximum 50 cities supported.")
        return [c.strip().title() for c in v]

    @model_validator(mode="after")
    def check_algorithm_city_limit(self):
        if self.algorithm == "brute_force" and len(self.cities) > 12:
            raise ValueError(
                "Brute force supports maximum 12 cities. "
                "Use algorithm='nearest_neighbor' or 'auto' for larger sets."
            )
        return self


# ── Response Models ─────────────────────────────────────────────────────────

class RouteResult(BaseModel):
    route: list[str]
    distance_km: int


class OptimizeResponse(BaseModel):
    best_route: list[str]
    total_distance_km: int
    all_routes: list[RouteResult]
    cities_count: int
    routes_checked: int
    algorithm_used: str
    note: str | None = None


class DistanceResponse(BaseModel):
    city1: str
    city2: str
    distance_km: int


class CitiesResponse(BaseModel):
    cities: list[str]


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
  
