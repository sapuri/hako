from django.test import TestCase

from web.models import *


class RoomTests(TestCase):
    @staticmethod
    def create_room(room_id: str = 'test', name: str = 'test', user_id: str = 'test',
                    ip_addr: str = '127.0.0.1') -> object:
        return Room.objects.create(room_id=room_id, name=name, user_id=user_id, ip_addr=ip_addr)

    def test_room_creation(self):
        room = self.create_room()
        self.assertTrue(isinstance(room, Room))
        self.assertEqual(room.__str__(), room.name)

    def test_generate_user_id(self):
        user_id = Room.generate_user_id('test', '127.0.0.1')
        self.assertEqual(len(user_id), 10)


class PostTests(TestCase):
    def setUp(self):
        self.room = RoomTests.create_room()

    @staticmethod
    def create_post(room: object, index: int = 1, name: str = '', body: str = 'test', user_id: str = 'test',
                    ip_addr: str = '127.0.0.1') -> object:
        return Post.objects.create(index=index, room=room, name=name, body=body, user_id=user_id, ip_addr=ip_addr)

    def test_post_creation(self):
        post = self.create_post(room=self.room)
        self.assertTrue(isinstance(post, Post))
        self.assertEqual(post.__str__(), post.name)
