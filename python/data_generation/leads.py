import random
import pandas as pd

from faker import Faker

fake = Faker("en_IN")

def generate_leads():

    destinations_df = pd.read_csv("output/destinations.csv")

    leads = []

    lead_id = 1

    for _ in range(15000):

        first_name = fake.first_name()

        last_name = fake.last_name()

        lead_name = f"{first_name} {last_name}"

        phone_number = fake.phone_number()

        email = fake.unique.email()

        city = fake.city()

        interested_destination = random.choice(
            destinations_df["destination_name"].tolist()
        )

        interested_trip_type = random.choices(
            [
                "Backpacking",
                "Luxury",
                "Weekend Getaway",
                "Adventure",
                "Spiritual",
                "Honeymoon",
                "Family",
                "Workation"
            ],
            weights=[18,12,22,12,10,8,12,6],
            k=1
        )[0]

        if interested_trip_type == "Backpacking":
            budget = random.randint(8000,18000)

        elif interested_trip_type == "Luxury":
            budget = random.randint(30000,70000)

        elif interested_trip_type == "Weekend Getaway":
            budget = random.randint(8000,18000)

        elif interested_trip_type == "Adventure":
            budget = random.randint(15000,30000)

        elif interested_trip_type == "Spiritual":
            budget = random.randint(10000,25000)

        elif interested_trip_type == "Honeymoon":
            budget = random.randint(30000,70000)

        elif interested_trip_type == "Family":
            budget = random.randint(20000,50000)

        else:
            budget = random.randint(18000,35000)

        travel_month = random.choices(
            [
                "January","February","March","April",
                "May","June","July","August",
                "September","October","November","December"
            ],
            weights=[8,6,6,5,10,12,4,4,6,12,14,13],
            k=1
        )[0]

        travellers_count = random.randint(1,6)

        lead_source = random.choices(
            [
                "Instagram",
                "Website",
                "Referral",
                "Google Search"
            ],
            weights=[40,30,15,15],
            k=1
        )[0]

        lead_status = random.choices(
            [
                "New",
                "Contacted",
                "Qualified",
                "Converted",
                "Lost"
            ],
            weights=[10,20,20,35,15],
            k=1
        )[0]

        lead_temperature = random.choices(
            [
                "Hot",
                "Warm",
                "Cold"
            ],
            weights=[40, 40, 20],
            k=1
        )[0]

        follow_up_count = random.choices(
            [
                0,
                1,
                2,
                3,
                4,
                5,
                6
            ],
            weights=[8, 12, 20, 20, 18, 14, 8],
            k=1
        )[0]

        if lead_status == "Lost":

            lost_reason = random.choices(
                [
                    "Budget Issue",
                    "Travel Dates Not Suitable",
                    "Booked with Competitor",
                    "No Response",
                    "Family Decision",
                    "Office Leave Not Approved",
                    "Payment Issue",
                    "Health Issue"
                ],
                weights=[30,15,15,15,10,5,5,5],
                k=1
            )[0]

        else:

            lost_reason = None

        if lead_status == "Converted":

            remarks = random.choice([
                "Customer confirmed the booking.",
                "Payment received successfully.",
                "Trip booked after follow-up.",
                "Customer finalized the package."
            ])

        elif lead_status == "Lost":

            remarks = f"Lead lost due to {lost_reason.lower()}."

        elif lead_status == "Qualified":

            remarks = random.choice([
                "Customer is interested and comparing packages.",
                "Quotation shared with the customer.",
                "Waiting for travel confirmation."
            ])

        elif lead_status == "Contacted":

            remarks = random.choice([
                "Customer requested a callback.",
                "Initial discussion completed.",
                "Follow-up scheduled."
            ])

        else:

            remarks = "New enquiry received."

        enquiry_date = fake.date_between(
            start_date="-3y",
            end_date="today"
        )

        leads.append(
            {
                "lead_id": lead_id,
                "lead_name": lead_name,
                "phone_number": phone_number,
                "email": email,
                "city": city,
                "interested_destination": interested_destination,
                "interested_trip_type": interested_trip_type,
                "budget": budget,
                "travel_month": travel_month,
                "travellers_count": travellers_count,
                "lead_source": lead_source,
                "lead_status": lead_status,
                "lead_temperature": lead_temperature,
                "follow_up_count": follow_up_count,
                "lost_reason": lost_reason,
                "remarks": remarks,
                "enquiry_date": enquiry_date
            }
        )

        lead_id += 1

    df = pd.DataFrame(leads)

    df.to_csv(
        "output/leads.csv",
        index=False
    )

    print("leads.csv generated successfully!")