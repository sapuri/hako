from django.shortcuts import resolve_url
from django.test import TestCase

from web.models import *


class TestIndex(TestCase):
    def test_get(self):
        resp = self.client.get(resolve_url('web:index'))
        self.assertEqual(resp.status_code, 200)

    def test_post(self):
        data = {'name': 'test'}
        resp = self.client.post(resolve_url('web:index'), data)
        self.assertEqual(resp.status_code, 302)


class TestRoom(TestCase):
    def setUp(self):
        self.room_id = Room.generate_room_id()
        ip_addr = '127.0.0.1'
        room = Room.objects.create(
            room_id=self.room_id,
            name='test',
            user_id=Room.generate_user_id(self.room_id, ip_addr),
            ip_addr=ip_addr
        )
        room.save()

    def test_get(self):
        resp = self.client.get(resolve_url('web:room', room_id=self.room_id))
        self.assertEqual(resp.status_code, 200)

    def test_post(self):
        data = {
            'name': 'test',
            'body': 'test'
        }
        resp = self.client.post(resolve_url('web:room', room_id=self.room_id), data=data)
        self.assertEqual(resp.status_code, 302)
