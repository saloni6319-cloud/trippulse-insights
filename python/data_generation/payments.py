import random
import string
import pandas as pd

from faker import Faker

fake = Faker("en_IN")

def generate_payments():

    bookings_df = pd.read_csv("output/bookings.csv")

    payments = []

    payment_id = 1

    for _, booking in bookings_df.iterrows():

        booking_timestamp = pd.to_datetime(
            booking["booking_timestamp"]
        )

        payment_date = (
            booking_timestamp +
            pd.Timedelta(
                days=random.randint(0, 3)
            )
        )

        payment_method = random.choices(
            [
                "UPI",
                "Credit Card",
                "Debit Card",
                "Net Banking",
                "Wallet"
            ],
            weights=[40, 25, 20, 10, 5],
            k=1
        )[0]

        if booking["booking_status"] == "Completed":

            payment_status = "Paid"

            amount_paid = booking["final_amount"]

            refund_amount = 0

        elif booking["booking_status"] == "Confirmed":

            payment_status = "Paid"

            amount_paid = booking["final_amount"]

            refund_amount = 0

        elif booking["booking_status"] == "Pending":

            payment_status = "Pending"

            amount_paid = 0

            refund_amount = 0

        elif booking["booking_status"] == "Cancelled":

            refund_type = random.choices(
                [
                    "Full",
                    "Partial",
                    "None"
                ],
                weights=[70, 20, 10],
                k=1
            )[0]

            amount_paid = booking["final_amount"]

            if refund_type == "Full":

                booking["booking_status"] = "Refunded"

                payment_status = "Refunded"

                refund_amount = booking["final_amount"]

        elif refund_type == "Partial":

            payment_status = "Partially Refunded"

            refund_percentage = random.randint(20,80)

            refund_amount = round(
                booking["final_amount"] *
                refund_percentage / 100,
                2
            )

        else:

            payment_status = "Paid"

            refund_amount = 0

        transaction_id = (
            "TPPAY" +
            "".join(
                random.choices(
                    string.ascii_uppercase +
                    string.digits,
                    k=10
                )
            )
        )

        currency = "INR"

        payments.append(
            {
                "payment_id": payment_id,
                "booking_id": booking["booking_id"],
                "payment_timestamp": payment_date,
                "payment_method": payment_method,
                "payment_status": payment_status,
                "transaction_id": transaction_id,
                "amount_paid": amount_paid,
                "refund_amount": refund_amount,
                "currency": currency
            }
        )

        payment_id += 1

    df = pd.DataFrame(payments)

    df.to_csv(
        "output/payments.csv",
        index=False
    )

    print(
        "payments.csv generated successfully!"
    )