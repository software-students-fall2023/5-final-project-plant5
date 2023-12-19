import pytest
import time
from flask import Flask
from flask_socketio import SocketIOTestClient

from flask.testing import FlaskClient
from unittest.mock import patch
from mongomock import MongoClient
from app import app, socketio, set_mongo_client, connect_to_mongo

# Mock the connect_to_mongo function to return a mongomock client
@patch('app.connect_to_mongo')
def test_index_route(mock_connect_to_mongo):
    mock_mongo_client = MongoClient()
    set_mongo_client(mock_mongo_client)

    mock_connect_to_mongo.side_effect = lambda mongo_client=None: connect_to_mongo(mongo_client)

    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200


# Test the registration route
def test_register_route():
    mock_mongo_client = MongoClient()
    set_mongo_client(mock_mongo_client)
    with patch('app.connect_to_mongo', side_effect=lambda mongo_client=None: connect_to_mongo(mongo_client)):
        client = app.test_client()

        # Test register route
        response = client.post('/register', data={'username': 'test_user', 'password': 'test_password'})
        assert response.status_code == 302  # Expected redirect status code

 
def test_login_route():
    mock_mongo_client = MongoClient()
    set_mongo_client(mock_mongo_client)

    with patch('app.connect_to_mongo', side_effect=lambda mongo_client=None: connect_to_mongo(mongo_client)):
        client = app.test_client()

        # Test login route with invalid credentials
        response = client.post('/login', data={'username': 'invalid_user', 'password': 'invalid_password'})
        print(response.data)
        assert response.status_code == 200  # Expected 200 status code

    with patch('app.accounts.find_one', return_value={'username': 'existing_user', 'password': 'existing_password'}):
        client = app.test_client()

        # Test login route with valid credentials
        response = client.post('/login', data={'username': 'existing_user', 'password': 'existing_password'})

        assert response.status_code == 302  # Expected redirect status code for successful login

def test_logout_route():
    mock_mongo_client = MongoClient()
    set_mongo_client(mock_mongo_client)

    with patch('app.connect_to_mongo', side_effect=lambda mongo_client=None: connect_to_mongo(mongo_client)):
        client = app.test_client()

        # Test logout route
        response = client.get('/logout')
        assert response.status_code == 302  # Expected redirect status code


# Test the socketio functionality
def test_socketio_handle_message():
    mock_mongo_client = MongoClient()
    set_mongo_client(mock_mongo_client)

    with patch('app.connect_to_mongo', side_effect=lambda mongo_client=None: connect_to_mongo(mongo_client)):
        # Create a SocketIO test client
        client = SocketIOTestClient(app, socketio)

        # Connect the test client to the SocketIO server
        client.connect()

        # Emit a 'message' event to trigger the handle_message function
        client.emit('message', {'text': 'Test message', 'username': 'test_user'})

        # Wait for the server to process the event
        time.sleep(1)

        # checks the recieved message
        received_messages = client.get_received()
        print(received_messages)
        assert received_messages[-1]['args'][0]['text'] == 'Test message'

        # Disconnect the client
        client.disconnect()


if __name__ == '__main__':
    pytest.main()
