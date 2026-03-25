# 🗺️ RouteIQ API

**RouteIQ** — Find the shortest delivery route across multiple cities.  
Built with FastAPI + Python. Supports brute-force and Nearest Neighbor Structure.

---

## Project Structure

```
routeiq/
└── backend/
    ├── main.py                     ← RouteIQ entry point
    ├── requirements.txt
    ├── data/
    │   └── distances.csv           ← City distance data
    ├── models/
    │   └── schemas.py              ← Pydantic request/response models
    ├── routers/
    │   └── route_optimizer.py      ← API endpoint handlers
    └── services/
        ├── location_manager.py     ← Input parsing & validation
        ├── distance_loader.py      ← CSV loader (cached at startup)
        ├── route_generator.py      ← Permutation engine
        ├── distance_calculator.py  ← Per-route distance math
        ├── optimizer.py            ← Brute force shortest route finder
        └── nearest_neighbor.py     ← Nearest Neighbor heuristic (Phase 2)
```

---

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server (from backend/ directory)
uvicorn main:app --reload --port 8000
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Service health check |
| POST | `/api/v1/optimize` | Find shortest route |
| GET | `/api/v1/cities` | List all available cities |
| GET | `/api/v1/distance?city1=X&city2=Y` | Distance between two cities |

---

## Algorithms

| Algorithm | Flag | City Limit | Complexity | Quality |
|-----------|------|------------|------------|---------|
| Auto (default) | `auto` | ≤ 50 | — | Best for size |
| Brute Force | `brute_force` | ≤ 12 | O(n!) | Guaranteed optimal |
| Nearest Neighbor | `nearest_neighbor` | ≤ 50 | O(n²) | Good heuristic |
| NN Multi-Start | `nearest_neighbor_multi_start` | ≤ 50 | O(n³) | Best heuristic |

---

## Example Request

```bash
curl -X POST http://localhost:8000/api/v1/optimize \
  -H "Content-Type: application/json" \
  -d '{"cities": ["Mumbai", "Pune", "Nashik"], "algorithm": "auto"}'
```

## Example Response

```json
{
  "best_route": ["Mumbai", "Pune", "Nashik", "Mumbai"],
  "total_distance_km": 530,
  "cities_count": 3,
  "routes_checked": 2,
  "algorithm_used": "brute_force",
  "note": "Guaranteed optimal result.",
  "all_routes": [
    { "route": ["Mumbai", "Pune", "Nashik", "Mumbai"], "distance_km": 530 },
    { "route": ["Mumbai", "Nashik", "Pune", "Mumbai"], "distance_km": 530 }
  ]
}
```

---

## Interactive Docs

Once running, visit:
- **Swagger UI** → http://localhost:8000/docs
- **ReDoc** → http://localhost:8000/redoc

---

## Available Cities

`Agra` `Ahmedabad` `Bangalore` `Chennai` `Delhi`
`Hyderabad` `Jaipur` `Mumbai` `Nashik` `Pune`

Add more cities by editing `data/distances.csv` — no code changes needed.

---

## Roadmap

| Phase | Status | Features |
|-------|--------|---------|
| Phase 1 | ✅ Done | Brute force, CSV, FastAPI |
| Phase 2 | ✅ Done | Nearest Neighbor, startup cache |
| Phase 3 | 🔜 Next | Parallel processing, PostgreSQL, Redis |
| Phase 4 | 🔜 Future | Docker, cloud deploy, React dashboard |

---

*RouteIQ — Built step by step, designed to scale.*
