import sys

import pandas as pd

bookings = pd.read_csv("output/bookings.csv")
customers = pd.read_csv("output/customers.csv")
destinations = pd.read_csv("output/destinations.csv")
trips = pd.read_csv("output/trips.csv")
booking_passengers = pd.read_csv("output/booking_passengers.csv")
payments = pd.read_csv("output/payments.csv")
reviews = pd.read_csv("output/reviews.csv")
marketing_campaigns = pd.read_csv("output/marketing_campaigns.csv")
employees = pd.read_csv("output/employees.csv")
customer_campaigns = pd.read_csv("output/customer_campaigns.csv")
leads = pd.read_csv("output/leads.csv")
lead_interactions = pd.read_csv("output/lead_interactions.csv")
trip_pricing = pd.read_csv("output/trip_pricing.csv")


report = open("output/validation_report.txt", "w")

sys.stdout = report

def validate_table(
    df,
    table_name,
    primary_key=None,
    unique_columns=None
):

    print("=" * 60)
    print(table_name.upper())
    print("=" * 60)

    print(f"Total Rows : {len(df)}")
    print(f"Total Columns : {len(df.columns)}")

    if primary_key:

        duplicates = df[primary_key].duplicated().sum()

        print(
            f"Duplicate {primary_key}: {duplicates}"
        )

    if unique_columns:

        for column in unique_columns:

            duplicates = df[column].duplicated().sum()

            print(
                f"Duplicate {column}: {duplicates}"
            )

    print("\nMissing Values")

    print(
        df.isnull().sum()
    )

    print("\n")

validate_table(
    customers,
    "Customers",
    "customer_id",
    ["email"]
)

validate_table(
    destinations,
    "Destinations",
    "destination_id",
    ["destination_name"]
)

validate_table(
    trips,
    "Trips",
    "trip_id",
    ["trip_name"]
)

validate_table(
    bookings,
    "Bookings",
    "booking_id"
)

validate_table(
    booking_passengers,
    "Booking Passengers",
    "passenger_id"
)

validate_table(
    payments,
    "Payments",
    "payment_id",
    ["transaction_id"]
)

validate_table(
    reviews,
    "Reviews",
    "review_id"
)

validate_table(
    marketing_campaigns,
    "Marketing Campaigns",
    "campaign_id"
)

validate_table(
    customer_campaigns,
    "Customer Campaigns",
    "customer_campaign_id"
)

validate_table(
    leads,
    "Leads",
    "lead_id"
)

validate_table(
    employees,
    "Employees",
    "employee_id",
    ["email"]
)

validate_table(
    lead_interactions,
    "Lead Interactions",
    "interaction_id"
)

print("=" * 60)
print("LEAD INTERACTION BUSINESS RULES")
print("=" * 60)

missing_followups = lead_interactions[
    (lead_interactions["follow_up_required"]) &
    (lead_interactions["next_follow_up_date"].isnull())
]

print(
    "Missing next_follow_up_date where follow_up_required = True:",
    len(missing_followups)
)

validate_table(
    trip_pricing,
    "Trip Pricing",
    "pricing_id"
)

print("=" * 60)
print("FOREIGN KEY VALIDATION")
print("=" * 60)

print(
    "Invalid Customer IDs:",
    len(
        set(bookings.customer_id)
        -
        set(customers.customer_id)
    )
)

print(
    "Invalid Trip IDs:",
    len(
        set(bookings.trip_id)
        -
        set(trips.trip_id)
    )
)

print(
    "Invalid Booking IDs (Passengers):",
    len(
        set(booking_passengers.booking_id)
        -
        set(bookings.booking_id)
    )
)

print(
    "Invalid Booking IDs (Payments):",
    len(
        set(payments.booking_id)
        -
        set(bookings.booking_id)
    )
)

print(
    "Invalid Booking IDs (Reviews):",
    len(
        set(reviews.booking_id)
        -
        set(bookings.booking_id)
    )
)

print(
    "Invalid Customer IDs (Campaigns):",
    len(
        set(customer_campaigns.customer_id)
        -
        set(customers.customer_id)
    )
)

print(
    "Invalid Campaign IDs:",
    len(
        set(customer_campaigns.campaign_id)
        -
        set(marketing_campaigns.campaign_id)
    )
)

print(
    "Invalid Lead IDs:",
    len(
        set(lead_interactions.lead_id)
        -
        set(leads.lead_id)
    )
)

print(
    "Invalid Employee IDs:",
    len(
        set(lead_interactions.employee_id)
        -
        set(employees.employee_id)
    )
)

print(
    "Invalid Trip IDs (Pricing):",
    len(
        set(trip_pricing.trip_id)
        -
        set(trips.trip_id)
    )
)

print(
    "Invalid Lead IDs (Bookings):",
    len(
        set(bookings.lead_id.dropna())
        -
        set(leads.lead_id)
    )
)

print(
    "\nTravel Date Before Booking:"
)

print(
    (
        pd.to_datetime(bookings.travel_date)
        <
        pd.to_datetime(bookings.booking_timestamp)
    ).sum()
)

merged = reviews.merge(
    bookings,
    on="booking_id"
)

merged["travel_date"] = pd.to_datetime(merged["travel_date"])
merged["review_date"] = pd.to_datetime(merged["review_date"])

invalid_reviews = merged[
    merged["review_date"] < merged["travel_date"]
]

print(invalid_reviews[
    ["booking_id", "booking_status", "travel_date", "review_date"]
].head(20))

print("Invalid reviews:", len(invalid_reviews))

print(
    "\nReview Before Travel:"
)

print(
    (
        pd.to_datetime(merged.review_date)
        <
        pd.to_datetime(merged.travel_date)
    ).sum()
)

merged = payments.merge(
    bookings,
    on="booking_id"
)

print(
    "\nPayment Before Booking:"
)

print(
    (
        pd.to_datetime(
            merged.payment_timestamp
        )
        <
        pd.to_datetime(
            merged.booking_timestamp
        )
    ).sum()
)

print(
    "\nInvalid Ratings:"
)

print(
    (
        (reviews.rating < 1)
        |
        (reviews.rating > 5)
    ).sum()
)

print(
    "\nNegative Payments:"
)

print(
    (
        payments.amount_paid < 0
    ).sum()
)

print("\n" + "=" * 60)
print("DATA VALIDATION COMPLETED")
print("=" * 60)
print("PASS - CSV files loaded successfully")

sys.stdout = sys.__stdout__

report.close()

print("validation_report.txt generated successfully!")
