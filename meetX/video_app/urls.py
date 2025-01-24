from django.contrib import admin
from django.urls import path
from . import views
from .consumers import *
from .views import send_room_email


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.video_chat, name='video_chat'),
    path('ws/video_chat/', VideoChatConsumer.as_asgi()),
    path('send-room-email/', send_room_email, name='send_room_email'),

    
]