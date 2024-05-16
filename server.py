from flask import Flask, request
from pyfcm import FCMNotification

app = Flask(__name__)

@app.route('/send-notification', methods=['POST'])
def send_notification():
    data = request.get_json()

    push_service = FCMNotification(api_key="<Your-Server-Key>")

    registration_id = "<Device-registration-token>"
    message_title = data.get('title')
    message_body = data.get('body')

    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

    return result

if __name__ == '__main__':
    app.run(port=5000)