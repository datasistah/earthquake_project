import json
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('earthquake.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get all earthquake data
cursor.execute('SELECT * FROM earthquake')
earthquakes = cursor.fetchall()

# Convert data to the format our JavaScript expects
earthquake_list = []
for row in earthquakes:
    row_dict = dict(row)
    formatted_dict = {
        "Year": row_dict["Year"],
        "Month": row_dict["Month"], 
        "Date": row_dict["Date"],
        "Hours": row_dict["Hours"], 
        "Minutes": row_dict["Minutes"],
        "Tsunami": row_dict["Tsunami"],
        "Name": row_dict["Name"],
        "Latitude": row_dict["Latitude"],
        "Longitude": row_dict["Longitude"],
        "Depth": row_dict["FocalDepth"] if row_dict["FocalDepth"] is not None else 0,
        "Magnitude": row_dict["Magnitude"],
        "Deaths": row_dict["Deaths"],
        "Injuries": row_dict["Injuries"],
        "Damage_Mill": row_dict["Damage_Mill"]
    }
    earthquake_list.append(formatted_dict)

# Save as JSON file
with open('static/data/earthquake_data.json', 'w') as f:
    json.dump(earthquake_list, f)

print(f"Data exported successfully! {len(earthquake_list)} records saved to static/data/earthquake_data.json")
