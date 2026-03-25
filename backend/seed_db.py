import csv

from db.database import (
    Base,
    engine,
    SessionLocal
)

from db.models import CityDistance


Base.metadata.create_all(
    bind=engine
)

db = SessionLocal()

with open(
    "distances.csv",
    "r"
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        record = CityDistance(

            city1=row["city1"],

            city2=row["city2"],

            distance=int(
                row["distance"]
            )
        )

        db.add(record)

db.commit()

db.close()

print("Database seeded successfully")
