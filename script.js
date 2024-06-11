function sendTestNotification() {
    console.log('Sending test notification...');

    var url = 'https://norion-firebase-api.loca.lt/send-notification';

    var data = {
        title: 'Test Notification',
        body: 'This is a test notification from the WebView',
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
            'bypass-tunnel-reminder': '1',
            'User-Agent': 'WebView',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return response.json();
        } else {
            return response.text().then(text => {
                throw new Error('Expected JSON, got text: ' + text);
            });
        }
    })
    .then(data => {
        console.log('Test notification sent successfully:', data);
    })
    .catch(error => {
        console.error('Error sending test notification:', error);
    });
}

function toggleTheme() {
    const body = document.body;
    body.style.backgroundColor = body.style.backgroundColor === 'black' ? 'white' : 'black';
    body.style.color = body.style.color === 'white' ? 'black' : 'white';
}
