
# Create your views here.
# views.py
from django.shortcuts import render
from chat_app.views import *

def video_chat(request):
    return render(request, '/home/wac/video_conf/meetX/video_app/templates/video_chat.html')


def chat(request):
    return render(request,'/home/wac/video_conf/meetX/chat_app/templates/chat_app/chat.html')