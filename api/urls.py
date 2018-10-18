from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

app_name = 'api'

router = DefaultRouter()

router.register(r'rooms', RoomViewSet, base_name='room')
router.register(r'posts', PostViewSet, base_name='post')

urlpatterns = [
    path('', include(router.urls)),
]
