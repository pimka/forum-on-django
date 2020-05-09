from datetime import timedelta

from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.authentication import (BasicAuthentication,
                                           TokenAuthentication)
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated

from .models import ServiceToken, UserCredentialsModel, UserToken


class CustomTokenAuth(TokenAuthentication):
    model = None
    keyword = 'Bearer'

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(token=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        delta_time = timezone.now() - token.created
        delta_time = timedelta(minutes=30) - delta_time

        if delta_time < timedelta():
            token.delete()
            raise NotAuthenticated('Elapsing token')

        return (None, token)

class ServicesTokenAuth(CustomTokenAuth):
    model = ServiceToken

class AuthTokenAuth(CustomTokenAuth):
    model = UserToken

class UserAuth(BasicAuthentication):
    model = UserCredentialsModel

    def authenticate(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise AuthenticationFailed('Invalid credentials', code='authentication')
            else:
                return (user, None)

        else:
            raise AuthenticationFailed('Empty credentials')
