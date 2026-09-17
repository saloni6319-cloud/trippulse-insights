import random
import pandas as pd

from faker import Faker
from datetime import timedelta

fake = Faker("en_IN")

def generate_customer_campaigns():

    customers_df = pd.read_csv("output/customers.csv")
    campaigns_df = pd.read_csv("output/marketing_campaigns.csv")

    customer_campaigns = []

    customer_campaign_id = 1

    for _, customer in customers_df.iterrows():

        campaign = campaigns_df.sample(1).iloc[0]

        start_date = pd.to_datetime(
            campaign["start_date"]
        )

        end_date = pd.to_datetime(
            campaign["end_date"]
        )

        acquisition_date = fake.date_between(
            start_date=start_date.date(),
            end_date=end_date.date()
        )

        first_touch = random.choices(
            [
                "Organic Search",
                "Paid Ads",
                "Email",
                "Direct"
            ],
            weights=[35,40,10,15],
            k=1
        )[0]

        conversion_days = random.randint(0,30)

        conversion_date = (
            acquisition_date +
            timedelta(days=conversion_days)
        )

        customer_campaigns.append(
            {
                "customer_campaign_id": customer_campaign_id,
                "customer_id": customer["customer_id"],
                "campaign_id": campaign["campaign_id"],
                "acquisition_date": acquisition_date,
                "first_touch": first_touch,
                "conversion_date": conversion_date
            }
        )

        customer_campaign_id += 1

    df = pd.DataFrame(customer_campaigns)

    df.to_csv(
        "output/customer_campaigns.csv",
        index=False
    )

    print(
        "customer_campaigns.csv generated successfully!"
    )