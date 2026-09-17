import pandas as pd
import mysql.connector


# -----------------------------
# Load CSV
# -----------------------------

df = pd.read_csv("output/customer_campaigns.csv")

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
INSERT INTO customer_campaigns (
    customer_campaign_id,
    customer_id,
    campaign_id,
    acquisition_date,
    first_touch,
    conversion_date
)
VALUES (
    %s, %s, %s, %s, %s, %s
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
        f"Imported {min(i + batch_size, len(data))} / {len(data)} customer campaigns"
    )


# -----------------------------
# Close connection
# -----------------------------

cursor.close()
conn.close()

print("Customer campaigns imported successfully!")