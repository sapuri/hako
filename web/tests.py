from django.shortcuts import resolve_url
from django.test import TestCase

from .models import *


class ViewTest(TestCase):
    def test_index(self):
        res = self.client.get(resolve_url('web:index'))
        self.assertEqual(res.status_code, 200)

    def test_room(self):
        room_id = Room.generate_room_id()
        ip_addr = '127.0.0.1'
        room = Room.objects.create(
            room_id=room_id,
            name='test',
            user_id=Room.generate_user_id(room_id, ip_addr),
            ip_addr=ip_addr
        )
        room.save()

        res = self.client.get(resolve_url('web:room', room_id=room_id))
        self.assertEqual(res.status_code, 200)
