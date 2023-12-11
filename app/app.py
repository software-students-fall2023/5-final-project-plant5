from flask import Flask, render_template, request
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


@app.route("/")
def index():
    data = collection.find()
    return render_template("index.html", data=data)


@app.route("/add", methods=["POST"])
def add():
    text = request.form["text"]
    collection.insert_one({"text": text})
    return index()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
