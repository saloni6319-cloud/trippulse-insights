import random
import pandas as pd

from faker import Faker

fake = Faker("en_IN")

def generate_employees():

    employees = []

    employee_id = 1

    DEPARTMENTS = {
        "Sales": {
            "designation": [
                "Sales Executive",
                "Senior Sales Executive",
                "Sales Manager"
            ],
            "count": 12
        },

        "Marketing": {
            "designation": [
                "Marketing Executive",
                "Marketing Manager"
            ],
            "count": 4
        },

        "Operations": {
            "designation": [
                "Operations Executive",
                "Operations Manager"
            ],
            "count": 4
        },

        "Finance": {
            "designation": [
                "Finance Executive"
            ],
            "count": 2
        },

        "Customer Support": {
            "designation": [
                "Support Executive"
            ],
            "count": 3
        }
    }

    for department, details in DEPARTMENTS.items():

        for _ in range(details["count"]):

            first_name = fake.first_name()

            last_name = fake.last_name()

            employee_name = (
                f"{first_name} {last_name}"
            )

            designation = random.choice(
                details["designation"]
            )

            email = (
                first_name.lower()
                + "."
                + last_name.lower()
                + "@trippulse.com"
            )

            phone_number = fake.phone_number()

            joining_date = fake.date_between(
                start_date="-5y",
                end_date="today"
            )

            employment_status = random.choices(
                [
                    "Active",
                    "Inactive"
                ],
                weights=[90,10],
                k=1
            )[0]

            employees.append(
                {
                    "employee_id": employee_id,
                    "employee_name": employee_name,
                    "department": department,
                    "designation": designation,
                    "email": email,
                    "phone_number": phone_number,
                    "joining_date": joining_date,
                    "employment_status": employment_status
                }
            )

            employee_id += 1

    df = pd.DataFrame(employees)

    df.to_csv(
        "output/employees.csv",
        index=False
    )

    print(
        "employees.csv generated successfully!"
    )