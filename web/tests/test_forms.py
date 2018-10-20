from django.test import TestCase

from web.forms import *


class TestRoomForm(TestCase):
    def test_valid_room_form(self):
        data = {'name': 'test'}
        room_form = RoomForm(data=data)
        self.assertTrue(room_form.is_valid())

    def test_invalid_room_form(self):
        data = {'name': ''}
        room_form = RoomForm(data=data)
        self.assertFalse(room_form.is_valid())


class TestPostForm(TestCase):
    def test_valid_post_form(self):
        data = {
            'name': '',
            'body': 'test'
        }
        post_form = PostForm(data=data)
        self.assertTrue(post_form.is_valid())

    def test_invalid_post_form(self):
        data = {
            'name': '',
            'body': ''
        }
        post_form = PostForm(data=data)
        self.assertFalse(post_form.is_valid())
