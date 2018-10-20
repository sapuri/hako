from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import *


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'create_post':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, pk=None):
        queryset = Room.objects.all()
        room = get_object_or_404(queryset, room_id=pk)
        serializer = self.get_serializer(room)
        return Response(serializer.data)

    @action(detail=True)
    def get_posts(self, request, pk=None):
        room = get_object_or_404(Room, room_id=pk)
        posts = Post.objects.filter(room=room)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], name='Create Post')
    def create_post(self, request, pk=None):
        room = get_object_or_404(Room, room_id=pk)
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            posts = Post.objects.filter(room=room)
            name = '名無しさん'
            if 'name' in serializer.data and serializer.data['name']:
                name = serializer.data['name']
            ip_addr = Room.get_client_ip(request)

            new_post = Post.objects.create(
                index=posts.count() + 1,
                room=room,
                name=name,
                body=serializer.data['body'],
                user_id=Room.generate_user_id(room.room_id, ip_addr),
                ip_addr=ip_addr,
            )
            return Response(PostSerializer(new_post).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]
