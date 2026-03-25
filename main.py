from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import HealthResponse
from services.distance_loader import load_distances
from routers import route_optimizer

CSV_PATH = "data/distances.csv"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup: load the distance map ONCE into app.state.
    All requests share this single in-memory object — zero disk reads after boot.
    Shutdown: nothing to clean up (plain dict).
    """
    print("🚀 RouteIQ — Loading distance map into cache...")
    app.state.distance_map = load_distances(CSV_PATH)
    cities = set()
    for key in app.state.distance_map:
        cities.update(key)
    print(f"✅ RouteIQ cache ready — {len(app.state.distance_map)} routes, {len(cities)} cities loaded.")
    yield
    print("🛑 RouteIQ shutting down.")


app = FastAPI(
    title="RouteIQ API",
    description=(
        "RouteIQ — Find the shortest delivery route across multiple cities. "
        "Supports brute-force (≤10 cities) and Nearest Neighbor heuristic (≤50 cities). "
        "Built with FastAPI + Python."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Allow frontend / mobile clients to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Restrict to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(
    route_optimizer.router,
    prefix="/api/v1",
    tags=["Route Optimizer"],
)


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    """Confirm the API service is running."""
    return HealthResponse(
        status="ok",
        service="RouteIQ API",
        version="1.0.0",
    )
  
