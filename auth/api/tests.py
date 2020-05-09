from django.conf import settings
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import ServiceToken, UserCredentialsModel, UserToken


class ServiceTokenTest(APITestCase):
    CREDENTIALS = settings.SERVICES_CREDENTIALS
    model = ServiceToken

    def test_get_token(self):
        data = {
            "id": self.CREDENTIALS["auth"]['id'],
            'secret': self.CREDENTIALS['auth']['secret']
        }
        respone = self.client.post(reverse('tokens'), data)
        self.assertEqual(respone.status_code, 200)

    def test_check_token(self):
        token = self.model.objects.create()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.token}')
        response = self.client.get(reverse('tokens'))


class UserTokenTest(APITestCase):
    def setUp(self):
        self.userdata = {'username':'username', 'password':'password'}
        self.user = UserCredentialsModel.objects.create_user(**self.userdata)

    def test_get_token(self):
        response = self.client.post(reverse('login_user'), data=self.userdata)
        self.assertEqual(response.status_code, 200)

    def test_check_token(self):
        token = UserToken.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.token}')
        response = self.client.get(reverse('auth'))
        self.assertEqual(response.status_code, 200)
