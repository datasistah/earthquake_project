from flask import Flask, render_template, redirect, Response, jsonify
from flask_pymongo import PyMongo
from bson import json_util
import json
import sys, getopt, pprint
from flask_cors import CORS, cross_origin

# Create an instance of Flask
app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_ORIGINS'] = '*'

app.config["MONGO_URI"] = "mongodb://localhost:27017/earthquake_db"
mongo = PyMongo(app)

earthquake = mongo.db.earthquake
earthquake.drop()

with open('data/earthquake.json') as f:
    data = json.load(f)

    for row in data:
        try:    
            earthquake.insert(row)
        except:
            print(row)

@app.route("/all", methods=['GET'])
@cross_origin()
def all():

    alldb = earthquake
    allearthquakes = alldb.find()
    earthquakejson = json.loads(json_util.dumps(allearthquakes))

    return jsonify(earthquakejson)

@app.route("/filter/<year_arg>/<month_arg>/<country_arg>/<magnitude_arg>/<death_arg>/<yearmin_arg>/<yearmax_arg>", methods=["GET"])
def filtered(year_arg=None, month_arg=None, country_arg=None, magnitude_arg=None, death_arg=None, yearmin_arg=None, yearmax_arg=None):
    alldb = earthquake
    
    filter_dict = {}

    if year_arg != "Select All":
        filter_dict["Year"] = int(year_arg)
        
    if month_arg != "Select All":
        if month_arg == "January":
            filter_dict["Month"] = 1
        elif month_arg == "February":
            filter_dict["Month"] = 2
        elif month_arg == "March":
            filter_dict["Month"] = 3
        elif month_arg == "April":
            filter_dict["Month"] = 4
        elif month_arg == "May":
            filter_dict["Month"] = 5
        elif month_arg == "June":
            filter_dict["Month"] = 6
        elif month_arg == "July":
            filter_dict["Month"] = 7
        elif month_arg == "August":
            filter_dict["Month"] = 8
        elif month_arg == "September":
            filter_dict["Month"] = 9
        elif month_arg == "October":
            filter_dict["Month"] = 10
        elif month_arg == "November":
            filter_dict["Month"] = 11
        elif month_arg == "December":
            filter_dict["Month"] = 12

    if country_arg != "Select All":
        filter_dict["Name"] = str(country_arg)

    if magnitude_arg != "Select All":
        if magnitude_arg == "minor":
            filter_dict["Magnitude"] = {"$gte":3,"$lt":4}
        elif magnitude_arg == "light":
            filter_dict["Magnitude"] = {"$gte":4,"$lt":5}      
        elif magnitude_arg == "moderate":
            filter_dict["Magnitude"] = {"$gte":5,"$lt":6}
        elif magnitude_arg == "strong":
            filter_dict["Magnitude"] = {"$gte":6,"$lt":7} 
        elif magnitude_arg == "major":
            filter_dict["Magnitude"] = {"$gte":7,"$lt":8} 
        else:
            filter_dict["Magnitude"] = {"$gte":8}

    if death_arg != "Select All":
        if death_arg == "yes":
            filter_dict["Deaths"] = {"$gt":0}

    if yearmin_arg != "Select All" and yearmax_arg!= "Select All":
        filter_dict["Year"] = {"$gte":int(yearmin_arg), "$lte":int(yearmax_arg)}

    filterdata = alldb.find(filter_dict)

    filteredjson = json.loads(json_util.dumps(filterdata))

    return jsonify(filteredjson)



if __name__ == "__main__":
    app.run(debug=True)