from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'chat_app'  # Ensure the app_name is defined correctly


urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('file_transfer/', views.file_transfer, name='file_transfer'),
    path('create-room/', views.create_room_and_send_email, name='create_room'),
    path('room/<str:room_id>/', views.room, name='room'),  # Placeholder for the room view

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
