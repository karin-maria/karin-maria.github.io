import os
import json
from flask import Flask, request
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__)

print('FIREBASE_SERVICE_ACCOUNT:', os.getenv('FIREBASE_SERVICE_ACCOUNT'))

service_account_info = json.loads(os.getenv('FIREBASE_SERVICE_ACCOUNT'))

print('Service Account Info:', service_account_info)

cred = credentials.Certificate(service_account_info)

print('Credential:', cred)

firebase_admin.initialize_app(cred)

print('Firebase App Initialized!')

@app.route('/send-notification', methods=['POST'])
def send_notification():
    print('In send_notification!')

    jsondata = request.get_json()

    print('JSON Data:', jsondata)

    registration_token = 'ddRvgtPeRoOO5pF8L5n5wk:APA91bF7P6vT1SyzpQi5tEf9gAXqfThhK9JIJBhneeEbNN5HdvN8LW-d-fC8je6b3bCfLnpDxt1WnuMCkj4RK6ehIma-4k1p0SPg_moTddq_rjPSddbHzfZ5ZTKBaCd0pnbbnyJtJv7d'

    #message = messaging.Message(
    #    data={
    #        'title': jsondata.get('title'),
    #        'body': jsondata.get('body'),
    #    },
    #    token=registration_token,
    #)

    message = messaging.Message(
    notification=messaging.Notification(
        title=jsondata.get('title'),
        body=jsondata.get('body'),
    ),
    token=registration_token,
)

    print('Message:', message)

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)

    return response

@app.route('/test', methods=['GET'])
def test_endpoint():
    return "Endpoint is working!"

if __name__ == '__main__':
    app.run(port=5000)
