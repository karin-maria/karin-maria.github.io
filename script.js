function sendTestNotification() {

    console.log('Sending test notification...');

    var url = 'https://firebase-api.loca.lt/send-notification';

    var data = {
        title: 'Test Notification',
        body: 'This is a test notification from the WebView.',
    };

    fetch(url, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    console.log('Test notification sent!');
}

function toggleTheme() {
    const body = document.body;
    body.style.backgroundColor = body.style.backgroundColor === 'black' ? 'white' : 'black';
    body.style.color = body.style.color === 'white' ? 'black' : 'white';
}
