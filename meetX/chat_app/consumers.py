import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'chat_room'
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        # Check if the 'message' key exists
            if 'message' in data:
                message = data['message']
            
            # Broadcast message to group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message
                    }
                )
            else:
            # Send an error response to the client if 'message' is missing
                await self.send(text_data=json.dumps({
                    'error': "Key 'message' is missing in the received data."
                }))
        except json.JSONDecodeError:
        # Handle invalid JSON
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON data received.'
            }))

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

class FileTransferConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Create a room name or use unique identifiers
        self.room_name = "file_transfer_room"
        self.room_group_name = f'file_transfer_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket (file message)
    async def receive(self, text_data):
        try:
        # Parse the incoming JSON data
            text_data_json = json.loads(text_data)

        # Validate and process file transfer data
            if 'file_name' in text_data_json and 'file_data' in text_data_json:
                file_name = text_data_json['file_name']
                file_data = text_data_json['file_data']

            # Send file information to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'send_file',
                        'file_name': file_name,
                        'file_data': file_data,
                        'sender': self.channel_name,
                    }
                )
            else:
            # Handle unexpected data format
                await self.send(text_data=json.dumps({
                    'error': 'Invalid data format. Expected file_name and file_data.',
                }))

        except json.JSONDecodeError:
        # Handle JSON parsing errors
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON data received.',
            }))

    # Receive message from room group (send file to the clients)
    async def send_file(self, event):
        file_name = event['file_name']
        file_data = event['file_data']
        sender = event['sender']

        # Send file data to the WebSocket clients
        if sender == self.channel_name:
            # If the message is from the sender, show "File sent"
            await self.send(text_data=json.dumps({
                'message': f'File sent: {file_name}',
                'file_name': file_name,

                'file_data': file_data,  # File data to show download
                'file_action': 'sent',   # Indicate that the sender sent the file
            }))
        else:
            # If the message is from another user, show "Download file"
            await self.send(text_data=json.dumps({
                'message': f'File received: {file_name}',
                'file_name': file_name,
                'file_data': file_data,  # File data for downloading
                'file_action': 'receive',  # Indicate to show download option
            }))