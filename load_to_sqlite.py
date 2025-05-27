import csv
import sqlite3

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect('earthquake.db')
c = conn.cursor()

# Create table
c.execute('''
CREATE TABLE IF NOT EXISTS earthquake (
    Id INTEGER PRIMARY KEY,
    Year INTEGER,
    Month INTEGER,
    Date INTEGER,
    Hours INTEGER,
    Minutes INTEGER,
    Tsunami TEXT,
    Name TEXT,
    Latitude REAL,
    Longitude REAL,
    FocalDepth REAL,
    Magnitude REAL,
    Deaths INTEGER,
    Injuries INTEGER,
    Damage_Mill REAL
)
''')

# Clear table
c.execute('DELETE FROM earthquake')

# Read CSV and insert data
with open('data/NOAAEarthquaqesince1600.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        c.execute('''
            INSERT INTO earthquake (Id, Year, Month, Date, Hours, Minutes, Tsunami, Name, Latitude, Longitude, FocalDepth, Magnitude, Deaths, Injuries, Damage_Mill)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            int(row['Id']) if row['Id'] else None,
            int(row['Year']) if row['Year'] else None,
            int(row['Month']) if row['Month'] else None,
            int(row['Date']) if row['Date'] else None,
            int(row['Hours']) if row['Hours'] else None,
            int(row['Minutes']) if row['Minutes'] else None,
            row['Tsunami'],
            row['Name'],
            float(row['Latitude']) if row['Latitude'] else None,
            float(row['Longitude']) if row['Longitude'] else None,
            float(row['Focal Depth (km)']) if row['Focal Depth (km)'] else None,
            float(row['Magnitude']) if row['Magnitude'] else None,
            int(row['Deaths']) if row['Deaths'] else None,
            int(row['Injuries']) if row['Injuries'] else None,
            float(row['Damage $Mill']) if row['Damage $Mill'] else None
        ))

conn.commit()
conn.close()

print('Data loaded into earthquake.db')
