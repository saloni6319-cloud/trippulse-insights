import pandas as pd
import mysql.connector


# -----------------------------
# Load CSV
# -----------------------------

df = pd.read_csv("output/bookings.csv")

# Convert NaN values to Python None
# so MySQL receives them as SQL NULL
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
INSERT INTO bookings (
    booking_id,
    customer_id,
    trip_id,
    lead_id,
    booking_timestamp,
    travel_date,
    travelers_count,
    booking_status,
    booking_source,
    coupon_code,
    discount_percentage,
    final_amount
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s
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
        f"Imported {min(i + batch_size, len(data))} / {len(data)} bookings"
    )


# -----------------------------
# Close connection
# -----------------------------

cursor.close()
conn.close()

print("Bookings imported successfully!")