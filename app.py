from flask import Flask
from flask_cors import CORS
import sklearn
import pandas

app = Flask(__name__)

CORS(app)

@app.route("/")
def index():
    response = ""
    with open("hello.txt") as file:
        for line in file:
            response += line
    return response
