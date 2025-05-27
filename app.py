from flask import Flask, render_template, redirect, Response, jsonify, request
import sqlite3
import json
import sys, getopt, pprint
import os
from flask_cors import CORS, cross_origin

# Create an instance of Flask
app = Flask(__name__, static_url_path='', static_folder='static')

CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_ORIGINS'] = '*'


# Helper function to get SQLite connection or load from JSON if DB not available (Vercel)
def get_db_connection():
    # First, try to connect to SQLite (local development)
    try:
        conn = sqlite3.connect('earthquake.db')
        conn.row_factory = sqlite3.Row
        return conn
    except:
        # If SQLite fails (Vercel deployment), return None so we fall back to JSON
        return None
        
# Helper function to get all earthquake data (works both locally and on Vercel)
def get_all_earthquakes():
    conn = get_db_connection()
    
    # If we have a SQLite connection (local development)
    if conn:
        earthquakes = conn.execute('SELECT * FROM earthquake').fetchall()
        conn.close()
        # Convert rows to dicts with expected property names
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
        return earthquake_list
    
    # If we don't have a SQLite connection (Vercel deployment)
    else:
        # Load from static JSON file
        try:
            with open('static/data/earthquake_data.json', 'r') as f:
                return json.load(f)
        except:
            # If JSON file doesn't exist yet, return empty list
            return []

@app.route("/", methods=['GET',"post"])
def mainroute():
    return app.send_static_file("index.html")

@app.route("/all", methods=['GET'])
@cross_origin()
def all():
    # Use our helper function that works both locally and on Vercel
    earthquake_list = get_all_earthquakes()
    return jsonify(earthquake_list)

@app.route("/filter/<year_arg>/<month_arg>/<country_arg>/<magnitude_arg>/<death_arg>/<yearmin_arg>/<yearmax_arg>", methods=["GET"])
def filtered(year_arg=None, month_arg=None, country_arg=None, magnitude_arg=None, death_arg=None, yearmin_arg=None, yearmax_arg=None):
    conn = get_db_connection()
    
    if conn: 
        # We have SQLite, use SQL query (local development)
        query = "SELECT * FROM earthquake WHERE 1=1"
        params = []
        if year_arg != "Select All":
            query += " AND Year = ?"
            params.append(int(year_arg))
        if month_arg != "Select All":
            month_map = {"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
            query += " AND Month = ?"
            params.append(month_map.get(month_arg, 0))
        if country_arg != "Select All":
            query += " AND Name LIKE ?"
            params.append(f"%{country_arg}%")
        if magnitude_arg != "Select All":
            if magnitude_arg == "minor":
                query += " AND Magnitude >= 3 AND Magnitude < 4"
            elif magnitude_arg == "light":
                query += " AND Magnitude >= 4 AND Magnitude < 5"
            elif magnitude_arg == "moderate":
                query += " AND Magnitude >= 5 AND Magnitude < 6"
            elif magnitude_arg == "strong":
                query += " AND Magnitude >= 6 AND Magnitude < 7"
            elif magnitude_arg == "major":
                query += " AND Magnitude >= 7 AND Magnitude < 8"
            else:
                query += " AND Magnitude >= 8"
        if death_arg != "Select All":
            if death_arg == "yes":
                query += " AND Deaths > 0"
        if yearmin_arg != "Select All" and yearmax_arg != "Select All":
            query += " AND Year >= ? AND Year <= ?"
            params.append(int(yearmin_arg))
            params.append(int(yearmax_arg))
        
        cur = conn.execute(query, params)
        results = cur.fetchall()
        conn.close()
        
        # Format results
        filtered_list = []
        for row in results:
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
            filtered_list.append(formatted_dict)
    else:
        # No SQLite, filter the JSON data (Vercel deployment)
        all_earthquakes = get_all_earthquakes()
        filtered_list = []
        
        # Python filtering to match SQL query logic
        for quake in all_earthquakes:
            # Start with assuming it passes all filters
            include = True
            
            # Apply each filter
            if year_arg != "Select All" and quake.get("Year") != int(year_arg):
                include = False
            
            if month_arg != "Select All":
                month_map = {"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,
                            "July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
                if quake.get("Month") != month_map.get(month_arg, 0):
                    include = False
            
            if country_arg != "Select All":
                if not (country_arg.lower() in quake.get("Name", "").lower()):
                    include = False
            
            if magnitude_arg != "Select All":
                mag = quake.get("Magnitude")
                if magnitude_arg == "minor" and (mag < 3.0 or mag >= 4.0):
                    include = False
                elif magnitude_arg == "light" and (mag < 4.0 or mag >= 5.0):
                    include = False
                elif magnitude_arg == "moderate" and (mag < 5.0 or mag >= 6.0):
                    include = False
                elif magnitude_arg == "strong" and (mag < 6.0 or mag >= 7.0):
                    include = False
                elif magnitude_arg == "major" and (mag < 7.0 or mag >= 8.0):
                    include = False
                elif magnitude_arg == "great" and mag < 8.0:
                    include = False
            
            if death_arg != "Select All" and death_arg == "yes":
                if not quake.get("Deaths", 0) > 0:
                    include = False
            
            if yearmin_arg != "Select All" and yearmax_arg != "Select All":
                year = quake.get("Year")
                if not (year >= int(yearmin_arg) and year <= int(yearmax_arg)):
                    include = False
                    
            # If it passed all filters, add it to the results
            if include:
                filtered_list.append(quake)
    
    return jsonify(filtered_list)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)