import csv
import os
import json
import pandas as pd

earthquake_df = pd.read_csv("data/NOAAEarthquaqesince1600.csv")

earthquake_df["Name"]=earthquake_df["Name"].str.split(":", expand=True)[0]

earthquake_df.to_json(r'data\earthquake.json', orient='records')