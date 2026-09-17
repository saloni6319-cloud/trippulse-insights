import random
import pandas as pd

from faker import Faker
from datetime import timedelta

fake = Faker("en_IN")

def generate_lead_interactions():

    leads_df = pd.read_csv("output/leads.csv")
    employees_df = pd.read_csv("output/employees.csv")

    interactions = []

    interaction_id = 1

    sales_team = employees_df[
        employees_df["department"] == "Sales"
    ]

    for _, lead in leads_df.iterrows():

        if lead["lead_status"] == "New":
            interactions_count = random.randint(0,1)

        elif lead["lead_status"] == "Contacted":
            interactions_count = random.randint(1,2)

        elif lead["lead_status"] == "Qualified":
            interactions_count = random.randint(2,4)

        elif lead["lead_status"] == "Converted":
            interactions_count = random.randint(2,5)

        else:
            interactions_count = random.randint(2,6)

        for i in range(
            interactions_count
        ):

            employee = sales_team.sample(1).iloc[0]

            enquiry_date = pd.to_datetime(
                lead["enquiry_date"]
            )

            min_days = i * 2
            max_days = i * 5 + 2

            interaction_date = (
                enquiry_date +
                timedelta(
                    days=random.randint(min_days, max_days)
                )
            )

            interaction_type = random.choices(
                [
                    "Call",
                    "WhatsApp",
                    "Email",
                    "SMS"
                ],
                weights=[55,25,15,5],
                k=1
            )[0]

            if lead["lead_status"] == "Converted":

                customer_response = random.choice(
                    [
                        "Very Interested",
                        "Interested"
                    ]
                )

            elif lead["lead_status"] == "Qualified":

                customer_response = random.choice(
                    [
                        "Interested",
                        "Need More Information",
                        "Need Time"
                    ]
                )

            elif lead["lead_status"] == "Lost":

                customer_response = random.choice(
                    [
                        "Not Interested",
                        "No Response"
                    ]
                )

            else:

                customer_response = random.choice(
                    [
                        "Interested",
                        "Need Time",
                        "No Response"
                    ]
                )

            if customer_response in [
                "Need Time",
                "Need More Information",
                "Not Interested"
            ]:

                objection_category = random.choices(
                    [
                        "Budget Issue",
                        "Travel Date Issue",
                        "Need Customization",
                        "Competitor",
                        "Family Decision",
                        "Office Leave",
                        "Payment Issue",
                        "Health Issue",
                        "No Objection"
                    ],
                    weights=[30,20,10,10,10,8,5,4,3],
                    k=1
                )[0]

            else:

                objection_category = "No Objection"

            follow_up_required = (
                i < interactions_count - 1
            )

            if follow_up_required:

                next_follow_up_date = (
                    interaction_date +
                    timedelta(
                        days=random.randint(2,7)
                    )
                ).date()

            else:

                next_follow_up_date = None

            if lead["lead_status"] == "Converted":

                interaction_outcome = "Converted"

            elif lead["lead_status"] == "Lost":

                interaction_outcome = "Lost"

            elif follow_up_required:

                interaction_outcome = "Follow-up Scheduled"

            else:

                interaction_outcome = "Quotation Shared"

            REMARKS = {
                "Budget Issue": [
                    "Customer requested a lower-priced package.",
                    "Budget exceeds customer's expectation.",
                    "Waiting for salary before confirming."
                    ],

                "Travel Date Issue": [
                    "Requested a different departure date.",
                    "Office leave not approved yet.",
                    "Travel dates do not match schedule."
                    ],

                "Need Customization": [
                    "Customer requested a customized itinerary.",
                    "Asked to include extra sightseeing."
                    ],

                "Competitor": [
                    "Customer is comparing another travel company.",
                    "Waiting for competitor quotation."
                    ],

                "Family Decision": [
                    "Waiting for family confirmation.",
                    "Spouse approval pending."
                    ],

                "Office Leave": [
                    "Waiting for office leave approval.",
                    "Customer will confirm after leave approval."
                    ],

                "Payment Issue": [
                    "Requested EMI option.",
                    "Payment method discussion pending."
                    ],

                "Health Issue": [
                    "Customer postponed due to health reasons."
                    ],

                "No Objection": [
                    "Customer is interested in proceeding.",
                    "Quotation shared successfully.",
                    "Customer appreciated the itinerary.",
                    "Booking confirmed."
                    ]
                }

            remarks = random.choice(
                REMARKS[objection_category]
            )

            interactions.append(
                {
                    "interaction_id": interaction_id,
                    "lead_id": lead["lead_id"],
                    "employee_id": employee["employee_id"],
                    "interaction_date": interaction_date,
                    "interaction_type": interaction_type,
                    "customer_response": customer_response,
                    "objection_category": objection_category,
                    "follow_up_required": follow_up_required,
                    "next_follow_up_date": next_follow_up_date,
                    "interaction_outcome": interaction_outcome,
                    "remarks": remarks
                }
            )

            interaction_id += 1

    df = pd.DataFrame(interactions)

    df.to_csv(
        "output/lead_interactions.csv",
        index=False
    )

    print(
        "lead_interactions.csv generated successfully!"
    ) 