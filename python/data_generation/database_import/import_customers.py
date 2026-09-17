import pandas as pd
import mysql.connector

# Read CSV
df = pd.read_csv("output/customers.csv")

# Convert missing values to None (SQL NULL)
df = df.where(pd.notna(df), None)

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shreya#Savya12",
    database="trip_pulse_insights"
)

cursor = connection.cursor()

# SQL insert
sql = """
INSERT INTO customers (
    customer_id,
    first_name,
    last_name,
    gender,
    date_of_birth,
    email,
    phone_number,
    city,
    state,
    country,
    signup_date,
    acquisition_channel,
    traveller_profile,
    verification_status,
    loyalty_level
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Convert DataFrame rows to tuples
data = [tuple(row) for row in df.itertuples(index=False, name=None)]

# Insert in batches
batch_size = 1000

for i in range(0, len(data), batch_size):
    cursor.executemany(sql, data[i:i + batch_size])
    connection.commit()
    print(f"Inserted {min(i + batch_size, len(data))} / {len(data)}")

cursor.close()
connection.close()

print("Customers imported successfully!")