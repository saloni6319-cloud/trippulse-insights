import random
import pandas as pd

from faker import Faker
from constants import TRAVELLER_PROFILES_DISTRIBUTION

fake = Faker("en_IN")

def generate_customers():

    customers = []

    customer_id = 1

    for _ in range(10000):

        first_name = fake.first_name()

        last_name = fake.last_name()

        gender = random.choice(
            ["Male", "Female"]
        )

        email = fake.unique.email()

        phone_number = fake.phone_number()

        city = fake.city()

        state = fake.state()

        country = "India"

        date_of_birth = fake.date_of_birth(
            minimum_age=18,
            maximum_age=60
        )

        signup_date = fake.date_between(
            start_date="-5y",
            end_date="today"
        )

        acquisition_channel = random.choices(
            [
                "Instagram",
                "Website",
                "Referral",
                "Google Search"
            ],
            weights=[40, 30, 20, 10],
            k=1
        )[0]

        traveller_profile = random.choices(
            population=list(TRAVELLER_PROFILES_DISTRIBUTION.keys()),
            weights=list(TRAVELLER_PROFILES_DISTRIBUTION.values()),
            k=1
        )[0]

        verification_status = random.choices(
            [
                "Verified",
                "Pending"
            ],
            weights=[90, 10],
            k=1
        )[0]

        loyalty_level = random.choices(
            [
                "Bronze",
                "Silver",
                "Gold",
                "Platinum"
            ],
            weights=[70, 20, 8, 2],
            k=1
        )[0]

        customers.append(
            {
                "customer_id": customer_id,
                "first_name": first_name,
                "last_name": last_name,
                "gender": gender,
                "date_of_birth": date_of_birth,
                "email": email,
                "phone_number": phone_number,
                "city": city,
                "state": state,
                "country": country,
                "signup_date": signup_date,
                "acquisition_channel": acquisition_channel,
                "traveller_profile": traveller_profile,
                "verification_status": verification_status,
                "loyalty_level": loyalty_level
            }
        )

        customer_id += 1

    df = pd.DataFrame(customers)

    df.to_csv("output/customers.csv", index=False)

    print("customers.csv generated successfully!")

