from rest_framework import serializers

from web.models import *


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('room_id', 'name', 'user_id', 'created_at', 'modified_at')
        read_only_fields = ('room_id', 'user_id', 'created_at', 'modified_at')
        extra_kwargs = {
            'created_at': {'format': '%Y/%m/%d %H:%M:%S'},
            'modified_at': {'format': '%Y/%m/%d %H:%M:%S'}
        }


class PostSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('index', 'room', 'name', 'body', 'user_id', 'created_at', 'modified_at')
        read_only_fields = ('index', 'room', 'user_id', 'created_at', 'modified_at')
        extra_kwargs = {
            'name': {'required': False},
            'created_at': {'format': '%Y/%m/%d %H:%M:%S'},
            'modified_at': {'format': '%Y/%m/%d %H:%M:%S'}
        }
