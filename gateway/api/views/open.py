import requests
from django.conf import settings
from rest_framework import status
from rest_framework.views import Response

from .base import BaseView


__default_oauth2_conf = {
    'CLIENT_ID': '', 'CLIENT_SECRET': ''
}
OAUTH2 = getattr(settings, 'OAUTH2', __default_oauth2_conf)
CLIENT_ID = OAUTH2['CLIENT_ID']
CLIENT_SECRET = OAUTH2['CLIENT_SECRET']
ERRORS_FIELD = getattr(settings, 'ERRORS_FIELD', 'error')
__default_urls = {
    'token-oauth2': 'http://localhost:8080/oauth2/token/',
    'token-revoke-oauth2': 'http://localhost:8080/oauth2/revoke_token/',
    'exchange-code-oauth2': 'http://localhost:8080/oauth2/token/',
    'authenticate-oauth2': 'http://localhost:8080/v0/oauth2/logged-in',
    'authenticate': 'http://localhost:8080/v0/users/logged-in',
    'login': 'http://localhost:8080/v0/users/login',
    'auth-token': 'http://localhost:8080/v0/tokens',
}
URLS = getattr(settings, 'URLS', __default_urls)


class GetHeadingsView(BaseView):
    def get(self, request):
        self.info(request, 'getting all headings')
        user_uuid = self.getUserUUID(request)
        try:
            get_request = requests.get(
                self.URL['heading']+'/headings/', params=request.query_params)
            self.send_task('GET HEADINGS', user_uuid, after=get_request.json())
            return Response(get_request.json())

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err))


class GetConcreteHeadingView(BaseView):
    def get(self, request, head_uuid):
        self.info(request, f'get heading {head_uuid}')
        user_uuid = self.getUserUUID(request)
        try:
            get_request = requests.get(
                f"{self.URL['heading']}/heading/{head_uuid}/")
            self.send_task('GET HEADING', user_uuid, after=get_request.json())
            return Response(get_request.json(), get_request.status_code)
        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), get_request.status_code)


class GetTagsView(BaseView):
    def get(self, request):
        self.info(request, 'getting all tags')
        user_uuid = self.getUserUUID(request)
        try:
            get_request = requests.get(
                self.URL['tag']+'/tags/', params=request.query_params)
            self.send_task('GET TAGS', user_uuid, after=get_request.json())
            return Response(get_request.json())

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err))


class GetMessagesView(BaseView):
    def get(self, request):
        self.info(request, 'getting all messages')
        user_uuid = self.getUserUUID(request)
        try:
            get_request = requests.get(
                self.URL['message']+'/messages/', params=request.query_params)
            self.send_task('GET MESSAGES', user_uuid, after=get_request.json())
            return Response(get_request.json())

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err))


class GetConcreteMessageView(BaseView):
    def get(self, request, mes_uuid):
        self.info(request, f'get message {mes_uuid}')
        user_uuid = self.getUserUUID(request)
        try:
            get_request = requests.get(
                f"{self.URL['message']}/messages/{mes_uuid}/")
            self.send_task('GET MESSAGE', user_uuid, after=get_request.json())
            return Response(get_request.json(), get_request.status_code)
        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), get_request.status_code)


class UsersView(BaseView):
    def post(self, request):
        self.info(request, 'add new user')
        user_uuid = self.getUserUUID(request)
        try:
            post_request = requests.post(
                self.URL['user']+'/user/', request.data)
            self.send_task('POST USER', user_uuid,
                           after=post_request.json())
            return Response(post_request.json(), post_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), post_request.status_code)


class GetConcreteUserView(BaseView):
    def get(self, request, user_uuid):
        self.info(request, f'get user {user_uuid}')
        user_uuid = self.getUserUUID(request)
        try:
            get_request = requests.get(
                f"{self.URL['user']}/get_user/{user_uuid}/")
            self.send_task('GET USER', user_uuid, after=get_request.json())
            return Response(get_request.json(), get_request.status_code)
        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), get_request.status_code)


class GetHeadingMessagesView(BaseView):
    def get(self, request, head_uuid):
        self.info(request, f'get heading {head_uuid}')
        user_uuid = self.getUserUUID(request)
        try:
            get_request = requests.get(
                f"{self.URL['heading']}/heading/{head_uuid}/")
            self.send_task('GET HEADING', user_uuid, after=get_request.json())

            if get_request.status_code >= 200 and get_request.status_code < 300:
                get_mes_request = requests.get(
                    self.URL['message']+'/messages/', params={'heading': head_uuid})
                self.send_task('GET MESSAGES', user_uuid,
                               after=get_mes_request.json())

                return Response(get_mes_request.json(), get_mes_request.status_code)

            return Response({'error': 'Heading does not exist'}, status.HTTP_404_NOT_FOUND)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), status.HTTP_503_SERVICE_UNAVAILABLE)


class CodeExchangeView(BaseView):
    def get(self, request):
        self.info(request, f"exchange code")
        code = request.query_params.get('code')
        if not code:
            self.exception(request, "'code' not found")
            return Response(data={ERRORS_FIELD: "'code' not found"}, status=status.HTTP_400_BAD_REQUEST)

        data = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
                'grant_type': 'authorization_code', 'code': code}
        try:
            response = requests.post(URLS['exchange-code-oauth2'], data=data)
        except requests.RequestException as err:
            return {ERRORS_FIELD: str(err)}, 503
        return Response(data=response.json(), status=response.status_code)
