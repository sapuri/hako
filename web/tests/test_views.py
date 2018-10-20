from django.shortcuts import resolve_url
from django.test import TestCase

from web.models import *


class IndexTests(TestCase):
    def test_get(self):
        resp = self.client.get(resolve_url('web:index'))
        self.assertEqual(200, resp.status_code)

    def test_post(self):
        data = {'name': 'test'}
        resp = self.client.post(resolve_url('web:index'), data)
        self.assertEqual(302, resp.status_code)

    def test_post_ng(self):
        data = {'name': ''}
        resp = self.client.post(resolve_url('web:index'), data)
        self.assertEqual(200, resp.status_code)


class RoomTests(TestCase):
    def setUp(self):
        self.room_id = Room.generate_room_id()
        ip_addr = '127.0.0.1'
        Room.objects.create(
            room_id=self.room_id,
            name='test',
            user_id=Room.generate_user_id(self.room_id, ip_addr),
            ip_addr=ip_addr
        )

    def test_get(self):
        resp = self.client.get(resolve_url('web:room', room_id=self.room_id))
        self.assertEqual(200, resp.status_code)

    def test_post(self):
        data = {
            'name': 'test',
            'body': 'test'
        }
        resp = self.client.post(resolve_url('web:room', room_id=self.room_id), data=data)
        self.assertEqual(302, resp.status_code)
