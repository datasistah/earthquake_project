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

# @app.route("/year/<int:year_arg>", methods=["GET"])
# def filtered(year_arg=None):
#     filter_data  = [] # copy
#     if year_arg != None:
#         filter_data = filter_data.find()

#     if mag != None:
#         pass

#     if country != None:
#         pass

#     return json_data



if __name__ == "__main__":
    app.run(debug=True)