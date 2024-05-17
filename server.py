import os
import json
from flask import Flask, request
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__)

# Initialize Firebase
def initFirebase():
    service_account_info = json.loads(os.getenv('FIREBASE_SERVICE_ACCOUNT'))
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred)

@app.route('/receive-token', methods=['POST'])
def receive_token():
    if not firebase_admin._apps:
        initFirebase()
    jsondata = request.get_json()
    registration_token = jsondata.get('token')

    print("Registration token received: ", registration_token)

    with open('.env', 'a') as file:
        file.write(f'FIREBASE_REGISTRATION_TOKEN={registration_token}\n')

    if registration_token is None:
        return 'No token found in request', 400

    return 'Token received successfully', 200

@app.route('/send-notification', methods=['POST'])
def send_notification():

    if not firebase_admin._apps:
        initFirebase()

    jsondata = request.get_json()

    message = messaging.Message(
        notification=messaging.Notification(
            title=jsondata.get('title'),
            body=jsondata.get('body'),
        ),
        token=os.getenv('FIREBASE_REGISTRATION_TOKEN') # registration_
    )

    response = messaging.send(message)
    return response

@app.route('/test', methods=['GET'])
def test_endpoint():
    return "Endpoint is working!"

if __name__ == '__main__':
    app.run(port=5000)
