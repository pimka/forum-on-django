import requests
from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError

from .models import User

ERRORS_FIELD = getattr(settings, 'ERRORS_FIELD', 'error')
__default_urls = {
    'login': 'http://localhost:8080/user/login',
}
URLS = getattr(settings, 'URLS', __default_urls)


class AuthBackend(ModelBackend):
    model = User
    ERRORS_FIELD = ERRORS_FIELD

    def authenticate_credentials(self, username, password):
        try:
            response = requests.post(URLS['login'], data={
                'username':username, 'password':password
            })
        except requests.RequestException as err:
            return { ERRORS_FIELD : str(err)}, 503
        
        return response.json(), response.status_code

    def authenticate(self, request, username=None, password=None, **kwargs):
        data, st = self.authenticate_credentials(username, password)

        if st != 200:
            msg = data.get(self.ERRORS_FIELD, f'auth respond status={st}')
            raise ValidationError(msg, code='authorization')

        try:
            user = self.model.objects.get(username=username)
        except self.model.DoesNotExist:
            user = self.model(username=username)

        user.is_superuser = data['is_superuser']
        user.is_staff = user.is_superuser
        user.save()

        return user
