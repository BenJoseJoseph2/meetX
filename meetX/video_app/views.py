
# Create your views here.
# views.py
from django.shortcuts import render

def video_chat(request):
    return render(request, '/home/wac/video_conf/meetX/video_app/templates/video_chat.html')
