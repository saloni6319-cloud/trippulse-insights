import random
import pandas as pd

from faker import Faker
from datetime import timedelta, date

fake = Faker("en_IN")

def generate_bookings():

    customers_df = pd.read_csv("output/customers.csv")
    trips_df = pd.read_csv("output/trips.csv")
    leads_df = pd.read_csv("output/leads.csv")

    converted_leads = leads_df[
        leads_df["lead_status"] == "Converted"
    ]

    converted_lead_ids = converted_leads["lead_id"].tolist()
    random.shuffle(converted_lead_ids)

    bookings = []

    booking_id = 1

    for _, customer in customers_df.iterrows():

        booking_option = random.choices(
            [0, 1, 2, 3],
            weights=[40, 40, 15, 5],
            k=1
        )[0]

        if booking_option == 3:
            bookings_count = random.randint(3, 6)
        else:
            bookings_count = booking_option

        for _ in range(bookings_count):

            suitable_trips = trips_df[
                trips_df["target_audience"].str.contains(
                    customer["traveller_profile"],
                    case=False,
                    na=False
                )
            ]

            trip = suitable_trips.sample(1).iloc[0]

            lead_id = None

            if random.random() < 0.45 and converted_lead_ids:
                lead_id = converted_lead_ids.pop()

            today = date.today()

            # 45% bookings are for trips that have already happened
            if random.random() < 0.45:

                booking_timestamp = fake.date_time_between(
                    start_date="-3y",
                    end_date="-60d"
                )

                travel_date = (
                    booking_timestamp +
                    timedelta(
                        days=random.randint(5, 60)
                    )
                ).date()

            # 55% bookings are for upcoming trips
            else:

                booking_timestamp = fake.date_time_between(
                    start_date="-90d",
                    end_date="now"
                )

                travel_date = (
                    booking_timestamp +
                    timedelta(
                        days=random.randint(10, 180)
                    )
                ).date()

            if trip["trip_type"] == "Honeymoon":
                travelers_count = 2

            elif trip["trip_type"] == "Backpacking":
                travelers_count = random.randint(1, 4)

            elif trip["trip_type"] == "Family":
                travelers_count = random.randint(3, 6)

            elif trip["trip_type"] == "Family Getaway":
                travelers_count = random.randint(3, 6)

            elif trip["trip_type"] == "Luxury":
                travelers_count = random.randint(2, 4)

            elif trip["trip_type"] == "Adventure":
                travelers_count = random.randint(1, 5)

            elif trip["trip_type"] == "Spiritual":
                travelers_count = random.randint(1, 5)

            elif trip["trip_type"] == "Weekend Getaway":
                travelers_count = random.randint(2, 5)

            elif trip["trip_type"] == "Workation":
                travelers_count = random.randint(1, 2)

            else:
                travelers_count = random.randint(1, 4)

            today = date.today()

            if travel_date <= today:

                booking_status = random.choices(
                    [
                        "Completed",
                        "Cancelled"
                    ],
                    weights=[85,15],
                    k=1
                )[0]

            else:

                booking_status = random.choices(
                    [
                        "Confirmed",
                        "Pending",
                        "Cancelled"
                    ],
                    weights=[75,15,10],
                    k=1
                )[0]

            booking_source = random.choices(
                [
                    "Website",
                    "Mobile App",
                    "Instagram",
                    "Referral Link"
                ],
                weights=[45, 35, 10, 10],
                k=1
            )[0]


            discount_percentage = random.choices(
                [
                    0,
                    5,
                    10,
                    15,
                    20
                ],
                weights=[65, 15, 10, 7, 3],
                k=1
            )[0]

            if discount_percentage == 0:
                coupon_code = None
            else:
                coupon_code = (
                    f"TP{discount_percentage}OFF"
                )

            subtotal = (
                trip["base_price"] *
                travelers_count
            )

            discount_amount = (
                subtotal *
                discount_percentage
            ) / 100

            final_amount = (
                subtotal -
                discount_amount
            )

            discount_amount = round(
                discount_amount,
                2
            )

            final_amount = round(
                final_amount,
                2
            )

            bookings.append(
                {
                    "booking_id": booking_id,
                    "customer_id": customer["customer_id"],
                    "trip_id": trip["trip_id"],
                    "lead_id": lead_id,
                    "booking_timestamp": booking_timestamp,
                    "travel_date": travel_date,
                    "travelers_count": travelers_count,
                    "booking_status": booking_status,
                    "booking_source": booking_source,
                    "coupon_code": coupon_code,
                    "discount_percentage": discount_percentage,
                    "final_amount": final_amount
                }
            )

            booking_id += 1

    df = pd.DataFrame(bookings)

    df.to_csv(
        "output/bookings.csv",
        index=False
    )

    print(
        "bookings.csv generated successfully!"
    )