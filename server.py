from flask import Flask, request

app = Flask(__name__)

@app.route('/send-notification', methods=['POST'])
def send_notification():

    jsondata = request.get_json()

    registration_token = 'ddRvgtPeRoOO5pF8L5n5wk:APA91bF7P6vT1SyzpQi5tEf9gAXqfThhK9JIJBhneeEbNN5HdvN8LW-d-fC8je6b3bCfLnpDxt1WnuMCkj4RK6ehIma-4k1p0SPg_moTddq_rjPSddbHzfZ5ZTKBaCd0pnbbnyJtJv7d'

    message = messaging.Message(
        data={
            'title': jsondata.get('title'),
            'body': jsondata.get('body'),
        },
        token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)

    return result

@app.route('/test', methods=['GET'])
def test_endpoint():
    return "Endpoint is working!"

if __name__ == '__main__':
    app.run(port=5000)