const grpname = JSON.parse(document.getElementById('group-name').textContent);

// when hosting on the ngrok platform use this URL.
// const ws = new WebSocket((window.location.protocol === 'https:' ? 'wss://' : 'ws://') + 'c6bf-2401-4900-530d-a04-2105-cda9-a2b7-955e.ngrok-free.app' + '/ws/' + grpname + '/'); {% endcomment %}

// other wise use this
const ws = new WebSocket('ws://' + window.location.host + '/ws/' + grpname + '/');

// Send message or file
function sendMessage() {
    const messageDom = document.getElementById('chat-message');
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];
    const message = messageDom.value.trim();

    if (message) {
        ws.send(JSON.stringify({
            'msg': message
        }));
        messageDom.value = ""; // Clear input field
    }

    if (file) {
        uploadFile(file);
    } else {
        console.log("No file to send.");
    }
}

// Handle incoming messages
ws.onmessage = function (event) {
    
    const chatMessage = JSON.parse(event.data);
    const chatWindow = document.querySelector('.chat-window');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', chatMessage.author === "{{ user.username }}" ? 'sent' : 'received');

    messageDiv.innerHTML = `
        <p>${chatMessage.msg}</p>
        <span class="user">${chatMessage.author === "{{ user.username }}" ? 'You' : chatMessage.author}</span>
      `;

    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to the latest message

};

ws.onerror = function (error) {
    console.error("WebSocket Error: ", error);
};

// File upload handling
function uploadFile(file) {
    const reader = new FileReader();
    reader.onload = () => {
        ws.send(reader.result); // Send binary file
    };
    reader.readAsArrayBuffer(file); // Read file as binary
}