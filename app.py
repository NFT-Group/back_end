from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(ap)

@app.route("/", methods=["POST"])
def index():
    return "Hello from the other heroku!"
