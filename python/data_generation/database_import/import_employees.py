import pandas as pd
import mysql.connector

df = pd.read_csv("output/employees.csv")
df = df.where(pd.notna(df), None)

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shreya#Savya12",
    database="trip_pulse_insights"
)

cursor = connection.cursor()

sql = """
INSERT INTO employees (
    employee_id,
    employee_name,
    department,
    designation,
    email,
    phone_number,
    joining_date,
    employment_status
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

data = [tuple(row) for row in df.itertuples(index=False, name=None)]

cursor.executemany(sql, data)
connection.commit()

print(f"Inserted {len(data)} / {len(data)}")
print("Employees imported successfully!")

cursor.close()
connection.close()