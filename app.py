from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import sklearn
import pandas
import pickle
import os.path
import json

app = Flask(__name__)

CORS(app)

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    collection = json.loads(str(request.data))["collection"]
    response += collection
    with open("hello.txt") as file:
        for line in file:
            response += line
    response += ". "
    if (os.path.exists("boredape_model.pkl")):
        response += "Bored ape model exists! 2"
    else:
        response += "Bored ape model does NOT exist."
    return response
