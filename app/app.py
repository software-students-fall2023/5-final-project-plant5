from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
import random
import colorsys
from datetime import datetime

app = Flask(__name__)
app.secret_key = "bobbykey"  # This the key for sessions


def connect_to_mongo():
    """
    This will attempt connect to the database.
    Returns:
        client: MongoDB client.
    """
    return MongoClient("mongodb://mongodb:27017/")


# MongoDB configuration
client = connect_to_mongo()
db = client["mydatabase"]

# check if the collection exists
if "mycollection" not in db.list_collection_names():
    # create the collection if it doesn't exist
    db.create_collection("mycollection")

collection = db["mycollection"]


if "accounts" not in db.list_collection_names():
    db.create_collection("accounts")

accounts = db["accounts"]


@app.route("/")
def index():
    session_username = session.get("username")
    data = collection.find()
    return render_template("index.html", data=data, session_username=session_username)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Check if the username exists in the accounts collection

        if accounts.find_one({"username": username}) is None:
            accounts.insert_one({"username": username, "password": password})

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    data2 = accounts.find()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if username/password combo exist in the accounts collection
        user = accounts.find_one({"username": username, "password": password})

        if user:
            # if so, we create a new session with name username
            session["username"] = username
            return redirect("/")

    return render_template("login.html", data2=data2)


@app.route("/logout")
def logout():
    session.clear()
    data = collection.find()
    return render_template("index.html", data=data)


@app.route("/add", methods=["POST"])
def add():
    text = request.form["text"]
    username = session.get("username")
    timestamp = datetime.now()
    collection.insert_one({"text": text, "username": username, "timestamp": timestamp})
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
