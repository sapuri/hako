import hashlib
import uuid

from django.db import models
from django.utils import timezone


class Room(models.Model):
    room_id = models.CharField('部屋ID', max_length=191, unique=True)
    name = models.CharField('部屋名', max_length=191)
    user_id = models.CharField('ユーザーID', max_length=191, help_text='作成者のユーザーID')
    ip_addr = models.GenericIPAddressField('IPアドレス', help_text='作成者のIPアドレス')
    is_active = models.BooleanField('有効', default=True)
    created_at = models.DateTimeField('作成日時', default=timezone.now)
    modified_at = models.DateTimeField('変更日時', auto_now=True)

    @staticmethod
    def generate_room_id() -> str:
        return uuid.uuid4().hex

    @staticmethod
    def generate_user_id(room_id: str, ip_addr: str) -> str:
        return hashlib.sha1(f'{room_id}{ip_addr}'.encode()).hexdigest()[:10]

    @staticmethod
    def get_client_ip(request: object) -> str:
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            ip_addr = xff.split(',')[0]
        else:
            ip_addr = request.META.get('REMOTE_ADDR')
        return ip_addr

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '部屋'
        verbose_name_plural = '部屋'


class Post(models.Model):
    index = models.IntegerField('番号')
    room = models.ForeignKey(Room, verbose_name='部屋', on_delete=models.CASCADE)
    name = models.CharField('名前', max_length=191)
    body = models.TextField('本文')
    user_id = models.CharField('ユーザーID', max_length=191)
    ip_addr = models.GenericIPAddressField('IPアドレス')
    is_active = models.BooleanField('有効', default=True)
    created_at = models.DateTimeField('作成日時', default=timezone.now)
    modified_at = models.DateTimeField('変更日時', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '投稿'
        verbose_name_plural = '投稿'
