import os
from functools import wraps

import requests
from django.conf import settings
from redis import StrictRedis
from requests.exceptions import RequestException

URLS = {
    'auth-token': os.environ.get('auth-token', 'http://localhost:8080/tokens/'),
    'user-stats': os.environ.get('user-stats', ''),
    'head-stats': os.environ.get('head-stats', 'http://localhost:8085/stat/'),
    'mes-stats': os.environ.get('mes-stats', ''),
}

ID = os.environ.get('APPID', 'stats')
SECRET = os.environ.get('APPSECRET', 'stats-secret')

TOKEN_LABEL = os.environ.get('TOKEN_LABEL', 'stats-service-token')

__default_redis_conf = {
    'host': 'localhost',
    'port': 6379, 'db': 0, 'password': None, 'decode_responses': True}
REDIS_CONF = os.environ.get('REDIS_CONF', __default_redis_conf)
STORAGE = StrictRedis(**REDIS_CONF)
ERRORS_FIELD = os.environ.get('ERRORS_FIELD', 'error')


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
            kwargs.update(
                {'headers': {'Authorization': f'{self.type} {self.token}'}})
            json, st = function(*args, **kwargs)

            if st not in [401, 402]:
                return (json, st)

        self.__update()
        kwargs.update(
            {'headers': {'Authorization': f'{self.type} {self.token}'}})

        return function(*args, **kwargs)


def token(id, secret):
    try:
        response = requests.post(
            URLS['auth-token'],
            {'id': id, 'secret': secret}
        )

    except RequestException:
        return ({ERRORS_FIELD: 'Connection failed'}, 503)

    return response.json(), response.status_code


@TokenAuthorize(storage=STORAGE, new=token, id=ID, secret=SECRET, token_label=TOKEN_LABEL)
def user_stats(data, headers):
    try:
        response = requests.post(
            url=URLS['user-stats'],
            data=data,
            headers=headers
        )

    except RequestException:
        return ({ERRORS_FIELD: 'Connection failed'}, 503)

    return response.json(), response.status_code


@TokenAuthorize(storage=STORAGE, new=token, id=ID, secret=SECRET, token_label=TOKEN_LABEL)
def head_stats(data, headers):
    print(f"data: {data}")
    try:
        response = requests.post(
            url=URLS['head-stats'],
            data=data,
            headers=headers
        )

    except RequestException:
        return ({ERRORS_FIELD: 'Connection failed'}, 503)

    return response.json(), response.status_code


def mes_stats(data, headers):
    try:
        response = requests.post(
            url=URLS['mes-stats'],
            data=data,
            headers=headers
        )

    except RequestException:
        return ({ERRORS_FIELD: 'Connection failed'}, 503)

    return response.json(), response.status_code
