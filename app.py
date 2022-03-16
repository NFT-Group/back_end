from flask import Flask
from flask_cors import CORS
import fs
import sklearn
import pandas

app = Flask(__name__)

CORS(app)

@app.route("/", methods=["POST"])
def index():
    response = ""
    with open("hello.txt") as file:
        for line in file:
            response += line
    return response
