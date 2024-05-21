import os
import json
from flask import Flask, request
import firebase_admin
from firebase_admin import credentials, messaging, auth

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
        print("Firebase initialized")
    else:
        print("Firebase already initialized")
    jsondata = request.get_json()
    fcmToken = jsondata.get('fcmToken')
    bank_id_token = jsondata.get('bankIdToken')
    firebaseIdToken = jsondata.get('firebaseIdToken')
    subscribed_to_notifications = jsondata.get('subscribed_to_notifications')

    print("fcmTokenreceived: ", fcmToken)
    print("Bank ID token received: ", bank_id_token)
    print("Firebase ID token received: ", firebaseIdToken)
    print("Subscribed to notifications: ", subscribed_to_notifications)

    with open('.env', 'a') as file:
        file.write(f'FIREBASE_REGISTRATION_TOKEN={fcmToken}\n')
        file.write(f'BANK_ID_TOKEN={bank_id_token}\n')

    if fcmToken is None or bank_id_token is None:
        return 'No token found in request', 400

    print("Decoding Firebase ID token")
    decoded_token = auth.verify_id_token(firebaseIdToken)
    uid = decoded_token['uid']

    # Set the custom claims
    print("Setting custom claims for user: ", uid)
    auth.set_custom_user_claims(uid, {'bankIdToken': bank_id_token})
    auth.set_custom_user_claims(uid, {'subscribedToNotifications': subscribed_to_notifications})
    print("Custom claims set for user: ", uid)
    print("Claims: ", auth.get_user(uid).custom_claims)

    return 'Token received successfully', 200

@app.route('/send-notification', methods=['POST'])
def send_notification():

    users = auth.list_users().iterate_all()
    print("Users: ", users)

    for user in users:
        print("User uid: ", user.uid)
        claims = user.custom_claims
        print("User claims: ", claims)


        if not firebase_admin._apps:
            initFirebase()
            print("Firebase initialized")
        else:
            print("Firebase already initialized")



        print("Sending notification to user: ", user.email)
        print("User subscribed to notifications: ", claims.get('subscribedToNotifications'))

        if claims.get('subscribedToNotifications'):
            message = messaging.Message(
                notification=messaging.Notification(
                    title=jsondata.get('title'),
                    body=jsondata.get('body'),
                ),
                token=os.getenv('FIREBASE_REGISTRATION_TOKEN'),
            )

        # Send the message
        response = messaging.send(message)
    return 'Notifications sent successfully', 200

@app.route('/test', methods=['GET'])
def test_endpoint():
    return "Endpoint is working!"

if __name__ == '__main__':
    app.run(port=5000)
