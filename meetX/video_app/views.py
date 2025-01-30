
# Create your views here.
# views.py
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def video_chat(request):
    return render(request, '/home/wac/video_conf/meetX/video_app/templates/video_app/video_chat.html')


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

# authentication starts
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'video_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('video_chat')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'video_app/login.html', {'form': form})

@login_required
def video_chat(request):
    return render(request, 'video_app/video_chat.html')

def logout_view(request):
    logout(request)  # Logs out the user and clears the session
    return redirect('login')  # Redirect to the login page after logout

# authentication ends
