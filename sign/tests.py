﻿# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
from sign.models import Event, Guest

# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1, name="oneplus 3 event", status=True, limit=2000, address='shenzhen',
                             start_time='2017-10-13 17:08:22.000000')
        Guest.objects.create(id=1, event_id=1, realname='alen', phone='13711001101', email='alen@mail.com',
                             sign=False)

    def test_event_models(self):
        result = Event.objects.get(name="oneplus 3 event")
        self.assertEqual(result.address, "shenzhen")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone="13711001101")
        self.assertEqual(result.realname, "alen")
        self.assertFalse(result.sign)

class IndexPageTest(TestCase):
    def test_index_page_renders_index_template(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

class LoginActionTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

    def test_add_admin(self):
        user = User.objects.get(username="admin")
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@mail.com")

    def test_login_action_username_password_null(self):
        test_data = {'username': '', 'password': ''}
        response = self.client.post('/login_action', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_username_password_error(self):
        test_data = {'username': 'abc', 'password': '123'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_success(self):
        test_data = {'username': 'admin', 'password': 'admin123'}
        response = self.client.post('/login_action', data=test_data)
        self.assertEqual(response.status_code, 302)

class EventMangeTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(name="xiaomi5", limit=2000, address='beijing', status=1, start_time='2017-8-10 12:30:00')
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)

    def test_add_event_data(self):
        event = Event.objects.get(name="xiaomi5")
        self.assertEqual(event.address, "beijing")

    def test_event_mange_success(self):
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)

    def test_event_mange_search_success(self):
        response = self.client.post('/search_name/', {"name": "xiaomi5"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)


class GuestManageTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(id=1,name="xiaomi5", limit=2000, address='beijing', status=1, start_time='2017-8-10 12:30:00')
        Guest.objects.create(realname="alen", phone=18611001100,email='alen@mail.com', sign=0, event_id=1)
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)

    def test_add_guest_data(self):
        guest = Guest.objects.get(realname="alen")
        self.assertEqual(guest.phone, "18611001100")
        self.assertEqual(guest.email, "alen@mail.com")
        self.assertFalse(guest.sign)

    def test_event_mange_success(self):
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alen", response.content)
        self.assertIn(b"18611001100", response.content)

    def test_guest_mange_search_success(self):
        response = self.client.post('/search_phone/', {"phone": "18611001100"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alen", response.content)
        self.assertIn(b"18611001100", response.content)


class SignIndexActionTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(id=1, name="xiaomi5", limit=2000, address='beijing', status=1, start_time='2017-8-10 12:30:00.000000')
        Event.objects.create(id=2, name="oneplus4", limit=2000, address='shenzhen', status=1, start_time='2017-6-10 12:30:00.000000')
        Guest.objects.create(realname="alen", phone=18611001100, email='alen@mail.com', sign=0, event_id=1)
        Guest.objects.create(realname="una", phone=18611001101, email='una@mail.com', sign=1, event_id=2)
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)

    def test_sign_index_action_phone_null(self):
        response = self.client.post('/sign_index_action/1/', {"phone": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"phone error.", response.content)

    def test_sign_index_action_phone_or_event_id_error(self):
        response = self.client.post('/sign_index_action/2/', {"phone": "18611001100"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"event id or phone error.", response.content)

    def test_sign_index_action_user_sign_has(self):
        response = self.client.post('/sign_index_action/2/', {"phone": "18611001101"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user has sign in.", response.content)

    def test_sign_index_action_sign_success(self):
        response = self.client.post('/sign_index_action/1/', {"phone": "18611001100"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"sign in success!", response.content)
