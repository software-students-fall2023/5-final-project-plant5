import json
from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO
from pymongo import MongoClient
from datetime import datetime
from bson import json_util


app = Flask(__name__)
app.secret_key = "bobbykey"
socketio = SocketIO(app)

def connect_to_mongo():
    return MongoClient("mongodb://mongodb:27017/")

client = connect_to_mongo()
db = client["mydatabase"]
messages_collection = db["messages"]
accounts = db["accounts"]

@app.route("/")
def index():
    session_username = session.get("username")
    messages = list(messages_collection.find())
    return render_template("index.html", messages=messages, session_username=session_username)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if accounts.find_one({"username": username}) is None:
            accounts.insert_one({"username": username, "password": password})
            return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = accounts.find_one({"username": username, "password": password})
        if user:
            session["username"] = username
            return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@socketio.on('message')
def handle_message(data):
    # Store the new message in the database
    new_message = {
        "text": data["text"],
        "username": data["username"],
        "timestamp": datetime.now()
    }
    messages_collection.insert_one(new_message)

    # Retrieve all messages from the database
    messages = list(messages_collection.find())

    # Format messages for JSON serialization
    formatted_messages = [{
        "text": msg["text"],
        "username": msg["username"],
        "timestamp": msg["timestamp"].strftime("%Y-%m-%d %H:%M:%S")  # Convert datetime to string
    } for msg in messages]

    # Emit the formatted messages to all clients
    socketio.emit('message', formatted_messages)

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", allow_unsafe_werkzeug=True)
