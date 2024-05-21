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
    firebaseIdToken = jsondata.get('firebaseIdToken')
    subscribedToNotifications = jsondata.get('subscribedToNotifications')

    print("fcmTokenreceived: ", fcmToken)
    print("Firebase ID token received: ", firebaseIdToken)
    print("Subscribed to notifications: ", subscribedToNotifications)


    if fcmToken is None or firebaseIdToken is None or subscribedToNotifications is None:
        return 'No token found in request', 400

    print("Decoding Firebase ID token")
    decoded_token = auth.verify_id_token(firebaseIdToken)
    uid = decoded_token['uid']

    print("USER EMAIL: ", decoded_token['email'])

    # Set the custom claims
    print("Setting custom claims for user: ", uid)
    auth.set_custom_user_claims(uid, {'fcmToken': fcmToken, 'subscribedToNotifications': subscribedToNotifications})
    print("Custom claims set for user: ", uid)
    print("Claims: ", auth.get_user(uid).custom_claims)

    return 'Token received successfully', 200

@app.route('/send-notification', methods=['POST'])
def send_notification():

    jsondata = request.get_json()

    if not firebase_admin._apps:
        initFirebase()
        print("Firebase initialized")
    else:
        print("Firebase already initialized")

    users = auth.list_users().iterate_all()
    print("Users: ", users)
    user_count = sum(1 for _ in auth.list_users().iterate_all())
    print("Number of users: ", user_count)

    print("********** STARTING LOOP **********")
    for user in users:

        print("User uid: ", user.uid)
        print("Claims: ", auth.get_user(user.uid).custom_claims)

        claims = user.custom_claims
        print("User claims: ", claims)

        if claims is None or not claims.get('subscribedToNotifications'):
            print("User has not subscribed to notifications, skipping...")
            continue

        print("Sending notification to user: ", user.email)
        print("User subscribed to notifications: ", claims.get('subscribedToNotifications'))

        if claims.get('subscribedToNotifications') and claims.get('fcmToken') is not None:
            print("Sending notificaion now!!")
            message = messaging.Message(
                notification=messaging.Notification(
                    title=jsondata.get('title'),
                    body=jsondata.get('body'),
                ),
                token=claims.get('fcmToken'),
            )
            response = messaging.send(message)
            print("Sent message: ", message)

    return 'Notifications sent successfully', 200

@app.route('/test', methods=['GET'])
def test_endpoint():
    return "Endpoint is working!"

if __name__ == '__main__':
    app.run(port=5000)
