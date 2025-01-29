# routing.py
from django.urls import path
from .consumers import VideoChatConsumer

websocket_urlpatterns = [
    path('ws/video_chat/', VideoChatConsumer.as_asgi()),
    path('ws/video_chat/<str:room_name>/', VideoChatConsumer.as_asgi()),
]
