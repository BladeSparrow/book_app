import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username='fixtureuser', email='f@example.com', password='StrongPass1')


def test_register_success(api_client):
    url = '/api/accounts/register/'
    data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'Abcdef1!',
        'password2': 'Abcdef1!'
    }
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == 201
    assert User.objects.filter(username='newuser').exists()


def test_register_negative_cases(api_client):
    url = '/api/accounts/register/'
    resp = api_client.post(url, {'username': ''}, format='json')
    assert resp.status_code == 400

    resp = api_client.post(url, {'username':'u','email':'u@e.com','password':'Abcdef1!','password2':'Different1!'}, format='json')
    assert resp.status_code == 400

    resp = api_client.post(url, {'username':'u2','email':'u2@e.com','password':'123','password2':'123'}, format='json')
    assert resp.status_code == 400

    resp = api_client.post(url, {'username':'u3','email':'not-an-email','password':'Abcdef1!','password2':'Abcdef1!'}, format='json')
    assert resp.status_code == 400


def test_login_and_refresh_and_logout(api_client, user):
    login_url = '/api/accounts/login/'
    refresh_url = '/api/accounts/token/refresh/'
    logout_url = '/api/accounts/logout/'

    resp = api_client.post(login_url, {'username': user.username, 'password': 'StrongPass1'}, format='json')
    assert resp.status_code == 200
    assert 'access' in resp.data and 'refresh' in resp.data
    import pytest
    from django.contrib.auth.models import User
    from rest_framework.test import APIClient


    @pytest.fixture
    def api_client():
        return APIClient()


    @pytest.fixture
    def user(db):
        return User.objects.create_user(username='fixtureuser', email='f@example.com', password='StrongPass1')


    def test_register_success(api_client):
        url = '/api/accounts/register/'
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'Abcdef1!',
            'password2': 'Abcdef1!'
        }
        resp = api_client.post(url, data, format='json')
        assert resp.status_code == 201
        assert User.objects.filter(username='newuser').exists()


    def test_register_negative_cases(api_client):
        url = '/api/accounts/register/'
        resp = api_client.post(url, {'username': ''}, format='json')
        assert resp.status_code == 400

        resp = api_client.post(url, {'username':'u','email':'u@e.com','password':'Abcdef1!','password2':'Different1!'}, format='json')
        assert resp.status_code == 400

        resp = api_client.post(url, {'username':'u2','email':'u2@e.com','password':'123','password2':'123'}, format='json')
        assert resp.status_code == 400

        resp = api_client.post(url, {'username':'u3','email':'not-an-email','password':'Abcdef1!','password2':'Abcdef1!'}, format='json')
        assert resp.status_code == 400


    def test_login_and_refresh_and_logout(api_client, user):
        login_url = '/api/accounts/login/'
        refresh_url = '/api/accounts/token/refresh/'
        logout_url = '/api/accounts/logout/'

        resp = api_client.post(login_url, {'username': user.username, 'password': 'StrongPass1'}, format='json')
        assert resp.status_code == 200
        assert 'access' in resp.data and 'refresh' in resp.data
        access = resp.data['access']
        refresh = resp.data['refresh']

        # refresh
        r2 = api_client.post(refresh_url, {'refresh': refresh}, format='json')
        assert r2.status_code == 200
        assert 'access' in r2.data

        # logout (idempotent)
        r = api_client.post(logout_url, {'refresh': refresh}, format='json')
        assert r.status_code in (200, 205)

        r2 = api_client.post(logout_url, {'refresh': refresh}, format='json')
        assert r2.status_code in (200, 205)

        # using blacklisted refresh should fail
        r3 = api_client.post(refresh_url, {'refresh': refresh}, format='json')
        assert r3.status_code != 200


    def test_login_failure_wrong_password(api_client, user):
        login_url = '/api/accounts/login/'
        resp = api_client.post(login_url, {'username': user.username, 'password': 'wrongpass'}, format='json')
        assert resp.status_code == 401