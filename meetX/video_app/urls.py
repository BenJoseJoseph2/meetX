from django.contrib import admin
from django.urls import path
from . import views
from .consumers import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('video_chat/', views.video_chat, name='video_chat'),
    path('ws/video_chat/', VideoChatConsumer.as_asgi()),
    
]