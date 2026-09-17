import pandas as pd
import mysql.connector

# Read CSV
df = pd.read_csv("output/leads.csv")

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

# SQL update
sql = """
UPDATE leads
SET
    lead_name = %s,
    phone_number = %s,
    email = %s,
    city = %s,
    interested_destination = %s,
    interested_trip_type = %s,
    budget = %s,
    travel_month = %s,
    travellers_count = %s,
    lead_source = %s,
    lead_status = %s,
    lead_temperature = %s,
    follow_up_count = %s,
    lost_reason = %s,
    remarks = %s,
    enquiry_date = %s
WHERE lead_id = %s
"""

# Reorder columns so lead_id comes last for the WHERE clause
data = [
    (
        row.lead_name,
        row.phone_number,
        row.email,
        row.city,
        row.interested_destination,
        row.interested_trip_type,
        row.budget,
        row.travel_month,
        row.travellers_count,
        row.lead_source,
        row.lead_status,
        row.lead_temperature,
        row.follow_up_count,
        row.lost_reason,
        row.remarks,
        row.enquiry_date,
        row.lead_id
    )
    for row in df.itertuples(index=False)
]

# Update in batches
batch_size = 1000

for i in range(0, len(data), batch_size):
    cursor.executemany(sql, data[i:i + batch_size])
    connection.commit()
    print(f"Updated {min(i + batch_size, len(data))} / {len(data)}")

cursor.close()
connection.close()

print("Leads updated successfully!")