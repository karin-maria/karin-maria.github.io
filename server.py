import os
import json
from flask import Flask, request
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__)

# Initialize Firebase
service_account_info = json.loads(os.getenv('FIREBASE_SERVICE_ACCOUNT'))
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

registration_token = None

@app.route('/receive-token', methods=['POST'])
def receive_token():
    jsondata = request.get_json()
    registration_token = jsondata.get('token')

    if registration_token is None:
        return 'No token found in request', 400

    # TODO: Store the token in your database

    return 'Token received successfully', 200

@app.route('/send-notification', methods=['POST'])
def send_notification():

    jsondata = request.get_json()

    #'ddRvgtPeRoOO5pF8L5n5wk:APA91bF7P6vT1SyzpQi5tEf9gAXqfThhK9JIJBhneeEbNN5HdvN8LW-d-fC8je6b3bCfLnpDxt1WnuMCkj4RK6ehIma-4k1p0SPg_moTddq_rjPSddbHzfZ5ZTKBaCd0pnbbnyJtJv7d'

    if registration_token is None:
        return 'No token found in request', 400

    message = messaging.Message(
        notification=messaging.Notification(
            title=jsondata.get('title'),
            body=jsondata.get('body'),
        ),
        token=registration_token,
    )

    response = messaging.send(message)
    return response

@app.route('/test', methods=['GET'])
def test_endpoint():
    return "Endpoint is working!"

if __name__ == '__main__':
    app.run(port=5000)
