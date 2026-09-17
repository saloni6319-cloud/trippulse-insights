import random
import pandas as pd

from faker import Faker
from datetime import timedelta

fake = Faker("en_IN")

def generate_trip_pricing():

    trips_df = pd.read_csv("output/trips.csv")

    pricing = []

    pricing_id = 1

    for _, trip in trips_df.iterrows():

        for quarter in range(4):

            year = 2026

            start_dates = [
                "2026-01-01",
                "2026-04-01",
                "2026-07-01",
                "2026-10-01"
            ]

            end_dates = [
                "2026-03-31",
                "2026-06-30",
                "2026-09-30",
                "2026-12-31"
            ]

            start_date = start_dates[quarter]

            end_date = end_dates[quarter]

            base_price = trip["base_price"]

            multiplier = {
                0: 1.05,
                1: 1.10,
                2: 0.95,
                3: 1.15
            }

            price = round(
                base_price *
                multiplier[quarter],
                2
            )

            discount_percentage = random.choices(
                [0,5,10,15,20],
                weights=[55,15,15,10,5],
                k=1
            )[0]

            today = pd.Timestamp.today()

            end = pd.to_datetime(end_date)

            start = pd.to_datetime(start_date)

            if end < today:

                pricing_status = "Expired"

            elif start > today:

                pricing_status = "Pending Approval"

            else:

                pricing_status = "Active"

            pricing.append(
                {
                    "pricing_id": pricing_id,
                    "trip_id": trip["trip_id"],
                    "start_date": start_date,
                    "end_date": end_date,
                    "price": price,
                    "discount_percentage": discount_percentage,
                    "pricing_status": pricing_status
                }
            )

            pricing_id += 1

            df = pd.DataFrame(pricing)

    df.to_csv(
        "output/trip_pricing.csv",
        index=False
    )

    print(
        "trip_pricing.csv generated successfully!"
    )