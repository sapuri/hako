from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from .views import *

app_name = 'api'

router = DefaultRouter()

router.register(r'rooms', RoomViewSet, base_name='room')
router.register(r'posts', PostViewSet, base_name='post')

schema_view = get_swagger_view(title='匣 API')

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', schema_view),
]
