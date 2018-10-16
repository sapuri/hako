from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from . import APP_NAME
from .models import *


class IndexView(View):
    template_name = f'{APP_NAME}/index.html'

    def get(self, request):
        context = {
            'title': '匣 - アカウント無しですぐに使える匿名プライベートチャットサービス'
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if 'action' in request.POST and request.POST['action'] == 'save':
            if 'room_name' in request.POST and request.POST['room_name']:
                room_name = request.POST.get('room_name')
                room_id = Room.generate_room_id()
                ip_addr = Room.get_client_ip(request)
                user_id = Room.generate_user_id(room_id, ip_addr)
                room = Room.objects.create(room_id=room_id, name=room_name, user_id=user_id, ip_addr=ip_addr)
                room.save()

                return redirect('web:room', room_id=room_id)

        context = {
            'title': '匣 - アカウント無しですぐに使える匿名プライベートチャットサービス'
        }
        return render(request, self.template_name, context)


class RoomView(View):
    template_name = f'{APP_NAME}/room.html'

    def get(self, request, room_id):
        room = get_object_or_404(Room, room_id=room_id)
        posts = Post.objects.filter(room=room)
        posts_num = posts.count()

        initial_post = {
            'index': 0,
            'name': '匣',
            'body': f'ID:{room.user_id} によって部屋が作成されました。',
            'created_at': room.created_at
        }

        context = {
            'title': room.name,
            'room': room,
            'posts': posts,
            'posts_num': posts_num,
            'initial_post': initial_post
        }
        return render(request, self.template_name, context)

    def post(self, request, room_id):
        room = get_object_or_404(Room, room_id=room_id)
        posts = Post.objects.filter(room=room)
        posts_num = posts.count()

        if 'action' in request.POST and request.POST['action'] == 'save':
            name = '名無しさん'
            body = ''
            ip_addr = Room.get_client_ip(request)

            if 'name' in request.POST and request.POST['name']:
                name = request.POST.get('name')

            if 'body' in request.POST and request.POST['body']:
                body = request.POST.get('body')

            # TODO: form.py で clean する
            if body:
                new_post = Post.objects.create(
                    index=posts_num + 1,
                    room=room,
                    name=name,
                    body=body,
                    user_id=Room.generate_user_id(room_id, ip_addr),
                    ip_addr=ip_addr
                )
                new_post.save()

        return redirect('web:room', room_id=room_id)
