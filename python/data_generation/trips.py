import random
import pandas as pd

from constants import DESTINATIONS, TRIP_TEMPLATES


def generate_trips():

    trips = []

    trip_id = 1

    for destination_index, destination in enumerate(DESTINATIONS, start=1):

        destination_type = destination["destination_type"]

        templates = TRIP_TEMPLATES.get(destination_type, [])

        for template in templates:

            if not template["is_active"]:
                continue

            trip_suffix = template["trip_suffix"]

            if isinstance(trip_suffix, list):
                trip_suffix = random.choice(trip_suffix)

            trip_name = f'{destination["destination_name"]} {trip_suffix}'

            duration_days = random.randint(
                template["duration_range"][0],
                template["duration_range"][1]
            )

            max_capacity = random.randint(
                template["capacity_range"][0],
                template["capacity_range"][1]
            )

            min_price, max_price = template["base_price_range"]

            base_price = random.randint(
                min_price,
                max_price
           )
            
            trips.append(
                {
                    "trip_id": trip_id,
                    "destination_id": destination_index,
                    "trip_name": trip_name,
                    "trip_type": template["trip_type"],
                    "duration_days": duration_days,
                    "max_capacity": max_capacity,
                    "base_price": base_price,
                    "difficulty_level": template["difficulty_level"],
                    "target_audience": ", ".join(template["target_audience"])
                    if isinstance(template["target_audience"], list)
                    else template["target_audience"],
                    "trip_status": template.get("trip_status", "Active")
                }
            )
            trip_id += 1
    df = pd.DataFrame(trips)

    df.to_csv("output/trips.csv", index=False)

    print("trips.csv generated successfully!")