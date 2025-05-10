from django.urls import path
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
    path('ws/file_transfer/', consumers.FileTransferConsumer.as_asgi()),  # New WebSocket for file transfer

]
