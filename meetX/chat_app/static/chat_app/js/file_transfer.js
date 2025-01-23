let chatSocket;

function initFileTransfer(wsUrl) {
    chatSocket = new WebSocket(wsUrl);

    const fileInput = document.querySelector('#file-input');
    const sendButton = document.querySelector('#file-send-btn');
    const fileMessages = document.querySelector('#file-messages');

    chatSocket.onmessage = function (event) {
        const data = JSON.parse(event.data);

        if (data.file_action === 'receive') {
            // Display the file download link
            const downloadLink = document.createElement('a');
            downloadLink.href = `data:application/octet-stream;base64,${data.file_data}`;
            downloadLink.download = data.file_name;
            downloadLink.textContent = `Download ${data.file_name}`;
            downloadLink.classList.add('file-download-link');

            // Append the download link to the file messages container
            const messageContainer = document.createElement('div');
            messageContainer.classList.add('file-message');
            messageContainer.appendChild(downloadLink);
            fileMessages.appendChild(messageContainer);
        } else if (data.file_action === 'sent') {
            const confirmation = document.createElement('p');
            confirmation.textContent = data.message; // File sent confirmation
            confirmation.classList.add('file-sent-message');
            fileMessages.appendChild(confirmation);
        } else if (data.error) {
            console.error(data.error); // Display error messages
        }
    };

    sendButton.addEventListener('click', () => {
        if (fileInput.files.length > 0 && chatSocket.readyState === WebSocket.OPEN) {
            const file = fileInput.files[0];
            const reader = new FileReader();

            reader.onload = () => {
                const fileData = reader.result.split(',')[1]; // Extract Base64 content
                chatSocket.send(JSON.stringify({
                    'file_name': file.name,
                    'file_data': fileData
                }));

                // Clear the file input after sending
                fileInput.value = '';
            };

            reader.readAsDataURL(file); // Convert file to base64
        } else {
            console.error('No file selected or WebSocket not open.');
        }
    });
}

// Initialize WebSocket connection for file transfer
initFileTransfer('ws://' + window.location.host + '/ws/file_transfer/');
