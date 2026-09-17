import random
import pandas as pd

from faker import Faker

fake = Faker("en_IN")

def generate_reviews():

    bookings_df = pd.read_csv("output/bookings.csv")

    reviews = []

    review_id = 1

    for _, booking in bookings_df.iterrows():

        if booking["booking_status"] != "Completed":
            continue

        print("Completed booking found:", booking["booking_id"])

        travel_date = pd.to_datetime(
            booking["travel_date"]
        )

        review_date = (
            travel_date +
            pd.Timedelta(
                days=random.randint(1,15)
            )
        )

        rating = random.choices(
            [5,4,3,2,1],
            weights=[45,30,15,7,3],
            k=1
        )[0]

        REVIEW_TITLES = [
            "Amazing Experience",
            "Wonderful Trip",
            "Highly Recommended",
            "Great Value",
            "Memorable Journey",
            "Excellent Service",
            "Fantastic Trip",
            "Worth Every Penny",
            "Good Experience",
            "Could Be Better"
        ]

        review_title = random.choice(REVIEW_TITLES)

        REVIEW_COMMENTS = [
            "The trip was very well organized.",
            "Hotels and transportation were excellent.",
            "Trip leader was extremely helpful.",
            "Beautiful destination and smooth experience.",
            "Will definitely travel again with TripPulse.",
            "Great itinerary and good value for money.",
            "Food and accommodation exceeded expectations.",
            "Everything was professionally managed.",
            "Enjoyed every moment of the journey.",
            "Overall a fantastic experience."
        ]

        review_comment = random.choice(REVIEW_COMMENTS)

        reviews.append(
            {
                "review_id": review_id,
                "booking_id": booking["booking_id"],
                "rating": rating,
                "review_title": review_title,
                "review_comment": review_comment,
                "review_date": review_date
            }
        )

        review_id += 1

    df = pd.DataFrame(reviews)

    df.to_csv(
        "output/reviews.csv",
        index=False
    )

    print(
        "reviews.csv generated successfully!"
    )