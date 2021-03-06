from functools import wraps

import requests
from django.conf import settings
from redis import StrictRedis
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated


URLS = getattr(settings, 'URLS')
ERRORS_FIELD = getattr(settings, 'ERRORS_FIELD', 'error')
__default_redis_conf = {
    'host': 'localhost',
    'port': 6379, 'db': 0, 'password': None, 'decode_responses': True}
REDIS_CONF = getattr(settings, 'REDIS_CONF', __default_redis_conf)
STORAGE = StrictRedis(**REDIS_CONF)

ID = getattr(settings, 'APPID', 'users')
SECRET = getattr(settings, 'APPSECRET', 'users8081')
TOKEN_LABEL = getattr(settings, 'TOKEN_LABEL', 'users-service-token')

class TokenAuth(TokenAuthentication):
    keyword = 'Bearer'
    
    def authenticate_credentials(self, key):
        data, st = self.authenticate(token=f"{self.keyword} {key}")

        if st != 200:
            return None
        
        if st == 200:
            data['token'] = key
            return (None, data)

        return None

    def authenticate(self, token):
        try:
            response = requests.get(URLS['auth-token'], headers={'Authentication': token})
        except requests.RequestException as err:
            return { ERRORS_FIELD : str(err)}, 503

        return response.json(), response.status_code

class TokenOAuth2(TokenAuthentication):
    keyword = 'Bearer'

    def authenticate_credentials(self, key):
        data, st = self.auth(key)

        if st != 200:
            msg = data.get('error', 'Invalid token')
            raise AuthenticationFailed(msg, 'authentication')

        data['token'] = key
        return (None, data)

    def auth(self, token):
        try:
            response = requests.get(
                URLS['authenticate-oauth2'], headers={'Authorization': f'{self.keyword} {token}'})
        except requests.RequestException as err:
            return {ERRORS_FIELD: str(err)}, 503

        return response.json(), response.status_code

    def authenticate(self, request):
        return super().authenticate(request)

class TokenAuthorize:
    def __init__(self, storage, new, id, secret, token_label='<service>-token', token_type='Bearer'):
        self.storage = storage
        self.new = new
        self.id = id
        self.secret = secret
        self.label = token_label
        self.type = token_type

    def __update(self):
        json, st = self.new(self.id, self.secret)
        if st == 200:
            self.token = json['token']

    @property
    def token(self):
        return self.storage.get(self.label)

    @token.setter
    def token(self, value):
        self.storage.set(self.label, value)

    def __call__(self, wrapped_func):
        return self.decorate(wrapped_func)

    def decorate(self, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            return self.call(function, *args, **kwargs)

        return wrapper

    def call(self, function, *args, **kwargs):
        if self.token:
            kwargs.update({ 'headers' : {'Authorization' : f'{self.type} {self.token}'} })
            json, st = function(*args, **kwargs)

            if st not in [401, 402]:
                return (json, st)

        self.__update()
        kwargs.update({ 'headers' : {'Authorization' : f'{self.type} {self.token}'} })
        
        return function(*args, **kwargs)

def token(id, secret):
    try:
        response = requests.post(URLS['auth-token'], {'id': id, 'secret': secret})

    except requests.RequestException as err:
        return ({ERRORS_FIELD: str(err)}, 503)

    return response.json(), response.status_code

@TokenAuthorize(STORAGE, token, ID, SECRET, TOKEN_LABEL)
def send_credentials(credentials, headers={}):
    try:
        response = requests.post(URLS['send-credentials'], credentials, headers=headers)
    except requests.RequestException as err:
        return ({ERRORS_FIELD: str(err)}, 503)

    return response.json(), response.status_code

@TokenAuthorize(STORAGE, token, ID, SECRET, TOKEN_LABEL)
def update_credentials(uuid, credentials, headers={}):
    try:
        response = requests.put(URLS['update-credentials'].format(uuid=uuid), credentials, headers=headers)
    except requests.RequestException as err:
        return ({ERRORS_FIELD: str(err)}, 503)

    return response.json(), response.status_code