
# Create your views here.
# views.py
from django.shortcuts import render
from chat_app.views import *
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings



def video_chat(request):
    return render(request, '/home/wac/Downloads/meetxproject/meetX/video_app/templates/video_app/video_chat.html')


def chat(request):
    return render(request,'/home/wac/video_conf/meetX/chat_app/templates/chat_app/chat.html')

@csrf_exempt
def send_room_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        room_id = data.get('roomId')

        if email and room_id:
            subject = "MEETX Room Invitation"
            message = f"You've been invited to join a room on MEETX.\n\nRoom ID: {room_id}\n\nJoin now!"
            sender = settings.EMAIL_HOST_USER  # Get sender email from settings

            try:
                send_mail(subject, message, sender, [email])
                return JsonResponse({'success': True, 'message': 'Email sent successfully'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)}, status=500)
        else:
            return JsonResponse({'success': False, 'message': 'Invalid data'}, status=400)
