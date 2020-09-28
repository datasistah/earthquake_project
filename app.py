from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import csv
import os
import json
import pandas as pd
import sys, getopt, pprint

# Create an instance of Flask
app = Flask(__name__)

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
