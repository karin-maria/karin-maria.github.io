function sendTestNotification() {

    var url = 'https://http://brotjefors.pythonanywhere.com/send-notification';
  
    // The data to send to the server-side script
    var data = {
      title: 'Test Notification',
      body: 'This is a test notification from the WebView.',
    };
  
    // Send the data to the server-side script
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
  }