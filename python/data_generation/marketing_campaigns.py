import random
import pandas as pd

from faker import Faker

fake = Faker("en_IN")


def generate_marketing_campaigns():

    campaigns = []

    campaign_id = 1

    for _ in range(30):

        CAMPAIGN_NAMES = [
            "Summer Escape",
            "Monsoon Madness",
            "Winter Wonderland",
            "Backpacking Bonanza",
            "Weekend Escape",
            "Adventure Awaits",
            "Honeymoon Special",
            "Spiritual Journey",
            "Family Vacation",
            "New Year Getaway",
            "Christmas Escape",
            "Early Bird Offer",
            "Flash Sale",
            "Festive Deals",
            "Diwali Dhamaka",
            "Republic Day Sale",
            "Independence Day Offer",
            "Long Weekend Sale",
            "Student Special",
            "Solo Explorer"
        ]

        start_date = fake.date_between(
            start_date="-3y",
            end_date="today"
        )

        campaign_name = (
            f"{random.choice(CAMPAIGN_NAMES)} {start_date.year} #{campaign_id}"
        )    

        platform = random.choices(
            [
                "Instagram",
                "Facebook",
                "Google Ads",
                "YouTube",
                "LinkedIn",
                "Email",
                "Referral",
                "Influencer"
            ],
            weights=[35, 15, 20, 8, 5, 7, 5, 5],
            k=1
        )[0]

        duration = random.randint(7, 45)

        end_date = (
            pd.to_datetime(start_date) +
            pd.Timedelta(days=duration)
        ).date()

        budget = random.randint(
            50000,
            1000000
        )

        today = pd.Timestamp.today().date()

        if end_date < today:

            campaign_status = "Completed"

        elif start_date > today:

            campaign_status = random.choice(
                [
                    "Draft",
                    "Scheduled"
                ]
            )

        else:

            campaign_status = random.choice(
                [
                    "Active",
                    "Paused"
                ]
            )

        campaigns.append(
            {
                "campaign_id": campaign_id,
                "campaign_name": campaign_name,
                "platform": platform,
                "start_date": start_date,
                "end_date": end_date,
                "budget": budget,
                "campaign_status": campaign_status
            }
        )

        campaign_id += 1

        df = pd.DataFrame(campaigns)

    df.to_csv(
        "output/marketing_campaigns.csv",
        index=False
    )

    print(
        "marketing_campaigns.csv generated successfully!"
    )