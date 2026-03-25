from .models import CityDistance


def get_all_distances(db):

    rows = db.query(
        CityDistance
    ).all()

    distance_map = {}

    for row in rows:

        distance_map[
            (row.city1, row.city2)
        ] = row.distance

    return distance_map
