from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.urls import reverse


def chat(request):
    return render(request, 'webrtc_app/chat.html')

def file_transfer(request):
    return render(request, 'webrtc_app/file_transfer.html')

# mail system configuration

# Function to generate a random room ID (for testing purpose)
def generate_room_id():
    return get_random_string(length=8)  # generates a random 8-character string

# View to create a room and send the email
def create_room_and_send_email(request):
    if request.method == 'POST':
        # Get the recipient emails from the form
        recipient_emails = request.POST.get('email')

        if recipient_emails:
            # Split the emails by comma and strip whitespace
            recipient_list = [email.strip() for email in recipient_emails.split(',') if email.strip()]

            if recipient_list:
                room_id = generate_room_id()
                room_link = request.build_absolute_uri(reverse('webrtc_app:room', args=[room_id]))

                subject = f'Your Meeting Room: {room_id}'
                message = f'Click the following link to join your room: {room_link}'
                from_email = settings.EMAIL_HOST_USER

                try:
                    send_mail(subject, message, from_email, recipient_list)
                    return JsonResponse({"success": True, "message": "Room link sent successfully to all recipients"})
                except Exception as e:
                    return JsonResponse({"success": False, "message": f"Failed to send email: {str(e)}"})

            return JsonResponse({"success": False, "message": "No valid email addresses provided"})

        return JsonResponse({"success": False, "message": "Recipient email(s) are required"})

    return render(request, 'webrtc_app/create_room.html')  # Render the form

# webrtc_app/views.py (add this)

def room(request, room_id):
    # This is just a placeholder for when the room link is clicked
    return render(request, 'webrtc_app/room.html', {'room_id': room_id})
