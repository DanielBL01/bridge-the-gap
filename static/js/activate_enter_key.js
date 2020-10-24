/*
Since this part of code is purely javascript based and does 
not relate to socketio, it's kept in a different file

When a user hits the enter key which is defined in the 
keycode as 13, the send button will be clicked 
*/

document.addEventListener('DOMContentLoaded', () => {
    let msg = document.querySelector('#user_message');
    msg.addEventListener('keyup', event => {
        if (event.keyCode === 13) {
            document.querySelector('#send_message').click();
        }
    })
})

document.addEventListener('DOMContentLoaded', () => {
    let msg = document.querySelector('#room-name');
    msg.addEventListener('keyup', event => {
        if (event.keyCode == 13) {
            document.querySelector('#create-room').click();
        }
    })
}) 