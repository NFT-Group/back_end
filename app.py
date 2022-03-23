from flask import Flask
from flask_cors import CORS
import sklearn
import pandas
import pickle
import firebase_admin
from firebase_admin import credentials, firestore, db
from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor

import pickle
import os.path

app = Flask(__name__)

CORS(app)

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    with open("hello.txt") as file:
        for line in file:
            response += line
    response += ". "
    if (os.path.exists("boredape_model.pkl")):
        response += "Bored ape model exists!"
    else:
        response += "Bored ape model does NOT exist."
    return response
