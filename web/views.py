import requests
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from . import APP_NAME
from .forms import *
from .models import *


class IndexView(View):
    template_name = f'{APP_NAME}/index.html'

    def get(self, request):
        room_form = RoomForm()

        context = {
            'title': '匣 - アカウント無しですぐに使える匿名プライベートチャットサービス',
            'room_form': room_form,
            'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        room_form = RoomForm()
        ip_addr = Room.get_client_ip(request)

        if 'g-recaptcha-response' in request.POST and self.verify_recaptcha(request.POST.get('g-recaptcha-response'),
                                                                            ip_addr):
            room_form = RoomForm(data=request.POST)
            if room_form.is_valid():
                room_name = room_form.cleaned_data.get('name')
                room_id = Room.generate_room_id()
                ip_addr = Room.get_client_ip(request)
                user_id = Room.generate_user_id(room_id, ip_addr)
                Room.objects.create(room_id=room_id, name=room_name, user_id=user_id, ip_addr=ip_addr)
                return redirect('web:room', room_id=room_id)

        else:
            print('Human verification failed.')

        context = {
            'title': '匣 - アカウント無しですぐに使える匿名プライベートチャットサービス',
            'room_form': room_form,
            'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
        }
        return render(request, self.template_name, context)

    @staticmethod
    def verify_recaptcha(response, remoteip):
        resp = requests.post('https://www.google.com/recaptcha/api/siteverify', {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': response,
            'remoteip': remoteip
        })
        print(resp.json())
        return resp.json()['success']


class RoomView(View):
    template_name = f'{APP_NAME}/room.html'

    def get(self, request, room_id):
        room = get_object_or_404(Room, room_id=room_id)
        posts = Post.objects.filter(room=room).order_by('index')
        posts_num = posts.count()
        post_form = PostForm()

        initial_post = {
            'index': 0,
            'name': '匣',
            'body': f'ID:{room.user_id} が部屋を作成しました。\nこの部屋の URL を知っている人のみが参加できます。',
            'created_at': room.created_at,
        }

        context = {
            'title': f'{room.name} - 匣',
            'room': room,
            'posts': posts,
            'posts_num': posts_num,
            'initial_post': initial_post,
            'post_form': post_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, room_id):
        room = get_object_or_404(Room, room_id=room_id)
        posts = Post.objects.filter(room=room)
        posts_num = posts.count()
        post_form = PostForm(data=request.POST)

        if post_form.is_valid():
            name = post_form.cleaned_data.get('name')
            if not name:
                name = '名無しさん'
            body = post_form.cleaned_data.get('body')
            ip_addr = Room.get_client_ip(request)

            Post.objects.create(
                index=posts_num + 1,
                room=room,
                name=name,
                body=body,
                user_id=Room.generate_user_id(room_id, ip_addr),
                ip_addr=ip_addr,
            )

        return redirect('web:room', room_id=room_id)
