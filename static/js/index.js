document.addEventListener('DOMContentLoaded', () => {
    // connect to the socket server
    const socket = io() //.connect('http://' + document.domain + ':' + location.port);

    // handle the 'connect' event
    socket.on('connect', () => {
        console.log('connected to server');
    });

    // handle the 'disconnect' event
    socket.on('disconnect', () => {
        console.log('disconnected from server');
    });

    // handle the 'message' event
    socket.on('message', (data) => {
        console.log('received message:', data);

        // display the message
        const messageElement = document.createElement('div');
        messageElement.innerHTML = `${data.username}: ${data.message}`;
        document.querySelector('#messages').appendChild(messageElement);
    });

    // handle the form submission
    document.querySelector('#message-form').addEventListener('submit', (event) => {
        event.preventDefault();

        // get the message text
        const message = document.querySelector('#input-message').value;

        // send the message to the server
        socket.emit('message', {message: message});

        // clear the input field
        document.querySelector('#input-message').value = '';
    });
});