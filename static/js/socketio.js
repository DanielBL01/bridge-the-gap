document.addEventListener('DOMContentLoaded', () => {
    // Connect to the socketio server
    const socket = io();

    const username = document.querySelector('#get-username').innerHTML;
    
    // Set default room to General
    let room = "General";
    joinRoom("General");

    // Display incoming messages to the chat room
    socket.on('message', data => {
        const p = document.createElement('p');
        const username = document.createElement('span');
        const time = document.createElement('span');
        const br = document.createElement('br');
        
        if (data.username) {
            username.innerHTML = data.username;
            time.innerHTML = data.time;
    
            p.innerHTML = username.outerHTML + br.outerHTML + data.msg + br.outerHTML + time.outerHTML;
            document.querySelector('#display-messages').append(p)
        } else {
            displayMessage(data.msg);
        } 
    });

    // Sends the message to the 'message' event handler on the server
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user_message').value,
            'username': username, 'room': room});

        // Clear input
        document.querySelector('#user_message').value = '';
    }

    // Room Selection to leave and join a new room
    document.querySelectorAll('#select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room) {
                msg = `You are already in the room: ${room}.`
                displayMessage(msg)
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }
    });

    // Sends data of the user and room to the 'join' event on the server
    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room});
        
        // Focus input field when user joins a room
        document.querySelector('#user_message').focus()
    }

    // Sends data of the user and room to the 'leave' event on the server
    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room});

        // Clear your messages
        document.querySelector('#display-messages').innerHTML = ''
    }

    function displayMessage(message) {
        const p = document.createElement('p');
        p.innerHTML = message;
        document.querySelector('#display-messages').append(p);
    }
})