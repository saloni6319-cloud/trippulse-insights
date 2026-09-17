import pandas as pd
import mysql.connector

df = pd.read_csv("output/marketing_campaigns.csv")
df = df.where(pd.notna(df), None)

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shreya#Savya12",
    database="trip_pulse_insights"
)

cursor = connection.cursor()

sql = """
INSERT INTO marketing_campaigns (
    campaign_id,
    campaign_name,
    platform,
    start_date,
    end_date,
    budget,
    campaign_status
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

data = [tuple(row) for row in df.itertuples(index=False, name=None)]

cursor.executemany(sql, data)
connection.commit()

print(f"Inserted {len(data)} / {len(data)}")
print("Marketing campaigns imported successfully!")

cursor.close()
connection.close()