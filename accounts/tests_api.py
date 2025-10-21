from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse


class AccountsAPITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # fixture user for login tests
        cls.username = 'fixtureuser'
        cls.password = 'StrongPass1'
        cls.user = User.objects.create_user(username=cls.username, email='f@example.com', password=cls.password)

    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/accounts/register/'
        self.login_url = '/api/accounts/login/'
        self.refresh_url = '/api/accounts/token/refresh/'
        self.logout_url = '/api/accounts/logout/'

    def test_register_success(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'Abcdef1!',
            'password2': 'Abcdef1!'
        }
        resp = self.client.post(self.register_url, data, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_negative_cases(self):
        # missing username
        resp = self.client.post(self.register_url, {'username': ''}, format='json')
        self.assertEqual(resp.status_code, 400)

        # password mismatch
        resp = self.client.post(self.register_url, {'username':'u','email':'u@e.com','password':'Abcdef1!','password2':'Different1!'}, format='json')
        self.assertEqual(resp.status_code, 400)

        # weak password
        resp = self.client.post(self.register_url, {'username':'u2','email':'u2@e.com','password':'123','password2':'123'}, format='json')
        self.assertEqual(resp.status_code, 400)

        # invalid email
        resp = self.client.post(self.register_url, {'username':'u3','email':'not-an-email','password':'Abcdef1!','password2':'Abcdef1!'}, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_login_success_and_refresh(self):
        resp = self.client.post(self.login_url, {'username': self.username, 'password': self.password}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access', resp.data)
        self.assertIn('refresh', resp.data)
        refresh = resp.data['refresh']

        # refresh should return new access
        r2 = self.client.post(self.refresh_url, {'refresh': refresh}, format='json')
        self.assertEqual(r2.status_code, 200)
        self.assertIn('access', r2.data)

    def test_login_fail_wrong_password(self):
        resp = self.client.post(self.login_url, {'username': self.username, 'password': 'wrongpass'}, format='json')
        # the view returns plain-text 401 on failure
        self.assertEqual(resp.status_code, 401)

    def test_logout_blacklist_and_idempotent(self):
        # login to obtain refresh
        resp = self.client.post(self.login_url, {'username': self.username, 'password': self.password}, format='json')
        self.assertEqual(resp.status_code, 200)
        refresh = resp.data['refresh']

        # logout should accept the refresh and return 205
        r = self.client.post(self.logout_url, {'refresh': refresh}, format='json')
        self.assertIn(r.status_code, (200, 205))

        # second logout with same token should still succeed (idempotent)
        r2 = self.client.post(self.logout_url, {'refresh': refresh}, format='json')
        self.assertIn(r2.status_code, (200, 205))

        # attempting to refresh with the blacklisted token should not return 200
        r3 = self.client.post(self.refresh_url, {'refresh': refresh}, format='json')
        self.assertNotEqual(r3.status_code, 200)

    def test_logout_without_refresh_is_ok(self):
        r = self.client.post(self.logout_url, {}, format='json')
        self.assertIn(r.status_code, (200, 205))
