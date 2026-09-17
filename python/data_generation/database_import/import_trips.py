import pandas as pd
import mysql.connector

df = pd.read_csv("output/trips.csv")
df = df.where(pd.notna(df), None)

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shreya#Savya12",
    database="trip_pulse_insights"
)

cursor = connection.cursor()

sql = """
INSERT INTO trips (
    trip_id,
    destination_id,
    trip_name,
    trip_type,
    duration_days,
    max_capacity,
    base_price,
    difficulty_level,
    target_audience,
    trip_status
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

data = [tuple(row) for row in df.itertuples(index=False, name=None)]

batch_size = 1000

for i in range(0, len(data), batch_size):
    cursor.executemany(sql, data[i:i + batch_size])
    connection.commit()
    print(f"Inserted {min(i + batch_size, len(data))} / {len(data)}")

cursor.close()
connection.close()

print("Trips imported successfully!")