import pandas as pd
import mysql.connector


# -----------------------------
# Load CSV
# -----------------------------

df = pd.read_csv("output/booking_passengers.csv")

# Convert NaN values to Python None
df = df.where(pd.notna(df), None)


# -----------------------------
# Connect to MySQL
# -----------------------------

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shreya#Savya12",
    database="trip_pulse_insights"
)

cursor = conn.cursor()


# -----------------------------
# Insert query
# -----------------------------

query = """
INSERT INTO booking_passengers (
    passenger_id,
    booking_id,
    passenger_name,
    date_of_birth,
    gender,
    id_type,
    id_verified,
    is_primary_traveller
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s
)
"""


# -----------------------------
# Prepare data
# -----------------------------

data = [
    tuple(row)
    for row in df.itertuples(index=False, name=None)
]


# -----------------------------
# Insert in batches
# -----------------------------

batch_size = 1000

for i in range(0, len(data), batch_size):

    batch = data[i:i + batch_size]

    cursor.executemany(query, batch)
    conn.commit()

    print(
        f"Imported {min(i + batch_size, len(data))} / {len(data)} passengers"
    )


# -----------------------------
# Close connection
# -----------------------------

cursor.close()
conn.close()

print("Booking passengers imported successfully!")