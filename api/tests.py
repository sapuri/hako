import collections
from django.utils import dateformat
from django.utils.timezone import get_current_timezone
from rest_framework.test import APITestCase

from web.models import Room, Post


class DocTests(APITestCase):
    def test_get(self):
        resp = self.client.get('/api/docs/')
        self.assertEqual(200, resp.status_code)


class RoomTests(APITestCase):
    def setUp(self):
        self.room = self.create_room()
        self.post = self.create_post(self.room)
        self.tz = get_current_timezone()

    @staticmethod
    def create_room(room_id: str = '', name: str = 'test', user_id: str = '',
                    ip_addr: str = '127.0.0.1') -> object:
        if not room_id:
            room_id = Room.generate_room_id()
        if not user_id:
            user_id = Room.generate_user_id(room_id, ip_addr)
        return Room.objects.create(room_id=room_id, name=name, user_id=user_id, ip_addr=ip_addr)

    @staticmethod
    def create_post(room: object, index: int = 1, name: str = 'test', body: str = 'test', user_id: str = 'test',
                    ip_addr: str = '127.0.0.1') -> object:
        return Post.objects.create(index=index, room=room, name=name, body=body, user_id=user_id, ip_addr=ip_addr)

    def test_get(self):
        resp = self.client.get(f'/api/rooms/{self.room.room_id}/')
        expected = {
            'room_id': self.room.room_id,
            'name': 'test',
            'user_id': self.room.user_id,
            'created_at': dateformat.format(self.room.created_at.astimezone(self.tz), 'Y/n/d H:i:s'),
            'modified_at': dateformat.format(self.room.created_at.astimezone(self.tz), 'Y/n/d H:i:s')
        }
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.data)

    def test_get_posts(self):
        resp = self.client.get(f'/api/rooms/{self.room.room_id}/get_posts/')
        expected = [collections.OrderedDict({
            'index': 1,
            'room': collections.OrderedDict({
                'room_id': self.room.room_id,
                'name': 'test',
                'user_id': self.room.user_id,
                'created_at': dateformat.format(self.room.created_at.astimezone(self.tz), 'Y/n/d H:i:s'),
                'modified_at': dateformat.format(self.room.created_at.astimezone(self.tz), 'Y/n/d H:i:s')
            }),
            'name': 'test',
            'body': 'test',
            'user_id': self.post.user_id,
            'created_at': dateformat.format(self.post.created_at.astimezone(self.tz), 'Y/n/d H:i:s'),
            'modified_at': dateformat.format(self.post.created_at.astimezone(self.tz), 'Y/n/d H:i:s')
        })]
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.data)

    def test_create_post(self):
        data = {
            'name': 'test',
            'body': 'test'
        }
        resp = self.client.post(f'/api/rooms/{self.room.room_id}/create_post/', data=data)
        self.assertEqual(201, resp.status_code)
        self.assertEqual(2, resp.data['index'])
        self.assertEqual(collections.OrderedDict({
            'room_id': self.room.room_id,
            'name': 'test',
            'user_id': self.room.user_id,
            'created_at': dateformat.format(self.room.created_at.astimezone(self.tz), 'Y/n/d H:i:s'),
            'modified_at': dateformat.format(self.room.created_at.astimezone(self.tz), 'Y/n/d H:i:s')
        }), resp.data['room'])
        self.assertEqual('test', resp.data['name'])
        self.assertEqual('test', resp.data['body'])

    def test_create_post_ng(self):
        data = {
            'name': 'test',
            'body': ''
        }
        resp = self.client.post(f'/api/rooms/{self.room.room_id}/create_post/', data=data)
        self.assertEqual(400, resp.status_code)
