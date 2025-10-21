from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class AccountsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/accounts/register/'
        self.login_url = '/api/accounts/login/'
        self.refresh_url = '/api/accounts/token/refresh/'
        self.logout_url = '/api/accounts/logout/'

    def test_register_login_refresh_logout_flow(self):
        
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Abcdef1!',
            'password2': 'Abcdef1!'
        }
        resp = self.client.post(self.register_url, data, format='json')
        self.assertEqual(resp.status_code, 201)

        
        resp = self.client.post(self.login_url, {'username': 'testuser', 'password': 'Abcdef1!'}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access', resp.data)
        self.assertIn('refresh', resp.data)
        access = resp.data['access']
        refresh = resp.data['refresh']

        
        protected_resp = self.client.get('/protected/', HTTP_AUTHORIZATION=f'Bearer {access}')
        self.assertEqual(protected_resp.status_code, 200)

        
        resp = self.client.post(self.refresh_url, {'refresh': refresh}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access', resp.data)

        
        resp = self.client.post(self.logout_url, {'refresh': refresh}, format='json', HTTP_AUTHORIZATION=f'Bearer {access}')
        self.assertIn(resp.status_code, (200, 205, 201,))

    def test_register_negative_cases(self):
        
        resp = self.client.post(self.register_url, {'username': ''}, format='json')
        self.assertEqual(resp.status_code, 400)

        
        resp = self.client.post(self.register_url, {'username':'u','email':'u@e.com','password':'Abcdef1!','password2':'Different1!'}, format='json')
        self.assertEqual(resp.status_code, 400)

        
        resp = self.client.post(self.register_url, {'username':'u2','email':'u2@e.com','password':'123','password2':'123'}, format='json')
        self.assertEqual(resp.status_code, 400)

        
        resp = self.client.post(self.register_url, {'username':'u3','email':'not-an-email','password':'Abcdef1!','password2':'Abcdef1!'}, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_books_permissions_require_auth(self):
        
        resp = self.client.post('/api/publishers/', {'name':'P'}, format='json')
        self.assertEqual(resp.status_code, 401)
