document.addEventListener('DOMContentLoaded', () => {
    // Connect to the socketio server
    var socket = io();

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

    // Send messages
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user_message').value,
            'username': username, 'room': room});

        // Clear input
        document.querySelector('#user_message').value = '';
    }

    // Room Selection
    document.querySelectorAll('#select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room) {
                msg = `You are already in the room ${room}.`
                displayMessage(msg)
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }
    });

    function displayMessage(message) {
        const p = document.createElement('p');
        p.innerHTML = message;
        document.querySelector('#display-messages').append(p);
    }

    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room});
    }

    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room});

        // Clear your messages
        document.querySelector('#display-messages').innerHTML = ''
    }
})
