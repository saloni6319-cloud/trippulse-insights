import random
import pandas as pd

from faker import Faker

fake = Faker("en_IN")

def generate_booking_passengers():

    bookings_df = pd.read_csv("output/bookings.csv")

    passengers = []

    passenger_id = 1

    for _, booking in bookings_df.iterrows():

        travelers_count = booking["travelers_count"]

        for traveler_number in range(travelers_count):

            first_name = fake.first_name()

            last_name = fake.last_name()

            full_name = f"{first_name} {last_name}"

            gender = random.choice(
                ["Male", "Female"]
            )

            date_of_birth = fake.date_of_birth(
                minimum_age=5,
                maximum_age=65
            )

            is_primary_traveller = (
                traveler_number == 0
            )

            id_type = random.choices(
                [
                    "Aadhaar",
                    "Passport",
                    "Driving License"
                ],
                weights=[70, 20, 10],
                k=1
            )[0]

            id_verified = random.choices(
                [
                    "Verified",
                    "Pending"
                ],
                weights=[95, 5],
                k=1
            )[0]

            passengers.append(
                {
                    "passenger_id": passenger_id,
                    "booking_id": booking["booking_id"],
                    "passenger_name": full_name,
                    "date_of_birth": date_of_birth,
                    "gender" : gender,
                    "id_type" : id_type,
                    "id_verified" : id_verified,
                    "is_primary_traveller": is_primary_traveller
                }
            )

            passenger_id += 1

    df = pd.DataFrame(passengers)

    df.to_csv(
        "output/booking_passengers.csv",
        index=False
    )

    print(
        "booking_passengers.csv generated successfully!"
    )