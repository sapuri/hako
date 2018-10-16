from django.urls import path

from .views import *

app_name = 'web'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('room/<room_id>/', RoomView.as_view(), name='room'),
]
