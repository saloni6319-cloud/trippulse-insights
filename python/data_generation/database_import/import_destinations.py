import pandas as pd
import mysql.connector

df = pd.read_csv("output/destinations.csv")
df = df.where(pd.notna(df), None)

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shreya#Savya12",
    database="trip_pulse_insights"
)

cursor = connection.cursor()

sql = """
INSERT INTO destinations (
    destination_id,
    destination_name,
    state,
    country,
    destination_type,
    destination_status,
    preferred_seasons
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

data = [tuple(row) for row in df.itertuples(index=False, name=None)]

batch_size = 1000

for i in range(0, len(data), batch_size):
    cursor.executemany(sql, data[i:i + batch_size])
    connection.commit()
    print(f"Inserted {min(i + batch_size, len(data))} / {len(data)}")

cursor.close()
connection.close()

print("Destinations imported successfully!")