from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)


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
    data = collection.find()
    return render_template("index.html", data=data)


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
    # Fetch data from MongoDB collection

    return render_template("login.html", data2=data2)


@app.route("/add", methods=["POST"])
def add():
    text = request.form["text"]
    collection.insert_one({"text": text})
    return index()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
