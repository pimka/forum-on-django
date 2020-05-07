import requests
from rest_framework import status
from rest_framework.views import Response

from ..auth import TokenOAuth2
from ..permissions import IsAuthenticate
from .base import BaseView
from django.conf import settings
from requests import RequestException


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
__default_oauth2_conf = {
    'CLIENT_ID': '', 'CLIENT_SECRET': ''
}
OAUTH2 = getattr(settings, 'OAUTH2', __default_oauth2_conf)
CLIENT_ID = OAUTH2['CLIENT_ID']
CLIENT_SECRET = OAUTH2['CLIENT_SECRET']
ERRORS_FIELD = getattr(settings, 'ERRORS_FIELD', 'error')


class RefreshTokenView(BaseView):
    authentication_classes = (TokenOAuth2,)
    permission_classes = (IsAuthenticate,)

    def post(self, request):
        self.info(request, 'refresh token')
        token = request.data.get('refresh_token')
        data = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
                'grant_type': 'refresh_token', 'refresh_token': token}

        try:
            response = requests.post(URLS['exchange-code-oauth2'], data)
        except RequestException as err:
            return {ERRORS_FIELD: str(err)}, 503

        return Response(response.json(), response.status_code)


class RevokeTokenView(BaseView):
    authentication_classes = (TokenOAuth2,)
    permission_classes = (IsAuthenticate,)

    def post(self, request):
        self.info(request, 'revoke token')
        token = request.auth.get('token')
        data = {'token': token, 'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET}
        try:
            response = requests.post(URLS['token-revoke-oauth2'], data)
        except RequestException as err:
            return {ERRORS_FIELD: str(err)}, 503

        json = response.json() if response.text else {}
        status = response.status_code

        return Response(json, status)


class PostHeadingsView(BaseView):
    authentication_classes = (TokenOAuth2,)
    permission_classes = (IsAuthenticate,)

    def post(self, request):
        self.info(request, 'add new heading')
        user_uuid = self.getUserUUID(request)
        token = request.auth.get('token')
        try:
            post_request = requests.post(
                self.URL['heading']+'/headings_add/', request.data, headers={'Authorization': f'Bearer {token}'})
            self.send_task('POST HEADING', user_uuid,
                           after=post_request.json())
            return Response(post_request.json(), post_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), post_request.status_code)


class ConcreteHeadingView(BaseView):
    authentication_classes = (TokenOAuth2,)
    permission_classes = (IsAuthenticate,)

    def patch(self, request, head_uuid):
        self.info(request, f'patch heading {head_uuid}')
        user_uuid = self.getUserUUID(request)
        token = request.auth.get('token')
        try:
            patch_request = requests.patch(
                f"{self.URL['heading']}/headings/{head_uuid}/", request.data, headers={'Authorization': f'Bearer {token}'})
            self.send_task('PATCH HEADING', user_uuid,
                           after=patch_request.json())
            return Response(patch_request.json(), patch_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), patch_request.status_code)

    def delete(self, request, head_uuid):
        self.info(request, f'deleting heading {head_uuid}')
        user_uuid = self.getUserUUID(request)
        try:
            delete_request = requests.delete(
                f"{self.URL['heading']}/headings/{head_uuid}/")
            self.send_task('DELETE HEADING', user_uuid)
            get_request = requests.get(
                f"{self.URL['message']}/messages/", params={'heading': head_uuid})

            for message in get_request.json():
                self.info(request, f'deleting message {message.uuid}')
                delete_mes_request = requests.delete(
                    f"{self.URL['message']}/messages/{message.uuid}/")
                self.send_task('DELETE MESSAGE', user_uuid)

            return Response(status=delete_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), status.HTTP_503_SERVICE_UNAVAILABLE)


class TagsView(BaseView):
    authentication_classes = (TokenOAuth2,)
    permission_classes = (IsAuthenticate,)

    def post(self, request):
        self.info(request, 'add new tag')
        user_uuid = self.getUserUUID(request)
        token = request.auth.get('token')
        try:
            post_request = requests.post(
                self.URL['tag']+'/tags_add/', request.data, headers={'Authorization': f'Bearer {token}'})
            self.send_task('POST TAG', user_uuid,
                           after=post_request.json())
            return Response(post_request.json(), post_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), post_request.status_code)


class ConcreteTagView(BaseView):
    authentication_classes = (TokenOAuth2,)
    permission_classes = (IsAuthenticate,)

    def get(self, request, tag_uuid):
        self.info(request, f'get tag {tag_uuid}')
        user_uuid = self.getUserUUID(request)
        token = request.auth.get('token')
        try:
            get_request = requests.get(
                f"{self.URL['tag']}/get_tags/{tag_uuid}/", headers={'Authorization': f'Bearer {token}'})
            self.send_task('GET TAG', user_uuid, after=get_request.json())
            return Response(get_request.json(), get_request.status_code)
        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), get_request.status_code)

    def patch(self, request, tag_uuid):
        self.info(request, f'patch tag {tag_uuid}')
        user_uuid = self.getUserUUID(request)
        token = request.auth.get('token')
        try:
            patch_request = requests.patch(
                f"{self.URL['tag']}/tags/{tag_uuid}/", request.data, headers={'Authorization': f'Bearer {token}'})
            self.send_task('PATCH TAG', user_uuid,
                           after=patch_request.json())
            return Response(patch_request.json(), patch_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), patch_request.status_code)

    def delete(self, request, tag_uuid):
        self.info(request, f'deleting tag {tag_uuid}')
        user_uuid = self.getUserUUID(request)
        token = request.auth.get('token')
        try:
            delete_request = requests.delete(
                f"{self.URL['tag']}/tags/{tag_uuid}/", headers={'Authorization': f'Bearer {token}'})
            self.send_task('DELETE TAG', user_uuid)

            return Response(status=delete_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), status.HTTP_503_SERVICE_UNAVAILABLE)


class MessagesView(BaseView):
    authentication_classes = (TokenOAuth2,)
    permission_classes = (IsAuthenticate,)

    def post(self, request):
        self.info(request, 'add new message')
        user_uuid = self.getUserUUID(request)
        token = request.auth.get('token')
        try:
            post_request = requests.post(
                self.URL['message']+'/messages/', request.data, headers={'Authorization': f'Bearer {token}'})
            self.send_task('POST MESSAGE', user_uuid,
                           after=post_request.json())
            return Response(post_request.json(), post_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), post_request.status_code)


class ConcreteMessageView(BaseView):
    authentication_classes = (TokenOAuth2,)
    permission_classes = (IsAuthenticate,)

    def patch(self, request, mes_uuid):
        self.info(request, f'patch message {mes_uuid}')
        user_uuid = self.getUserUUID(request)
        token = request.auth.get('token')
        try:
            patch_request = requests.patch(
                f"{self.URL['message']}/messages/{mes_uuid}/", request.data, headers={'Authorization': f'Bearer {token}'})
            self.send_task('PATCH MESSAGE', user_uuid,
                           after=patch_request.json())
            return Response(patch_request.json(), patch_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), patch_request.status_code)

    def delete(self, request, mes_uuid):
        self.info(request, f'deleting message {mes_uuid}')
        user_uuid = self.getUserUUID(request)
        token = request.auth.get('token')
        try:
            delete_request = requests.delete(
                f"{self.URL['message']}/messages/{mes_uuid}/", headers={'Authorization': f'Bearer {token}'})
            self.send_task('DELETE MESSAGE', user_uuid)

            return Response(status=delete_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), status.HTTP_503_SERVICE_UNAVAILABLE)


class ConcreteUserView(BaseView):
    authentication_classes = (TokenOAuth2,)
    permission_classes = (IsAuthenticate,)

    def patch(self, request, user_uuid):
        self.info(request, f'patch user {user_uuid}')
        user_uuid = self.getUserUUID(request)
        token = request.auth.get('token')
        try:
            patch_request = requests.patch(
                f"{self.URL['user']}/user/{user_uuid}/", request.data, headers={'Authorization': f'Bearer {token}'})
            self.send_task('PATCH USER', user_uuid,
                           after=patch_request.json())
            return Response(patch_request.json(), patch_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), patch_request.status_code)


class HeadingMessagesView(BaseView):
    authentication_classes = (TokenOAuth2,)
    permission_classes = (IsAuthenticate,)

    def post(self, request, head_uuid):
        self.info(request, f'get heading {head_uuid}')
        user_uuid = self.getUserUUID(request)
        token = request.auth.get('token')
        try:
            get_request = requests.get(
                f"{self.URL['heading']}/heading/{head_uuid}/", headers={'Authorization': f'Bearer {token}'})
            self.send_task('GET HEADING', user_uuid, after=get_request.json())

            if get_request.status_code >= 200 and get_request.status_code < 300:
                request.data['head_uuid'] = head_uuid
                post_mes_request = requests.post(
                    self.URL['message']+'/messages/', request.data, headers={'Authorization': f'Bearer {token}'})
                self.send_task('POST MESSAGE', user_uuid,
                               after=post_mes_request.json())

                return Response(post_mes_request.json(), post_mes_request.status_code)

            return Response({'error': 'Heading does not exist'}, status.HTTP_404_NOT_FOUND)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), status.HTTP_503_SERVICE_UNAVAILABLE)


class ConcreteHeadingMessageView(BaseView):
    authentication_classes = (TokenOAuth2,)
    permission_classes = (IsAuthenticate,)

    def get(self, request, head_uuid, mes_uuid):
        self.info(request, f'get heading {head_uuid}')
        user_uuid = self.getUserUUID(request)
        token = request.auth.get('token')
        try:
            get_request = requests.get(
                f"{self.URL['heading']}/heading/{head_uuid}/", headers={'Authorization': f'Bearer {token}'})
            self.send_task('GET HEADING', user_uuid, after=get_request.json())

            if get_request.status_code >= 200 and get_request.status_code < 300:
                get_mes_request = requests.get(
                    f"{self.URL['message']}/message/{mes_uuid}/", headers={'Authorization': f'Bearer {token}'})
                self.send_task('GET MESSAGE', user_uuid,
                               after=get_mes_request.json())

                return Response(get_mes_request.json(), get_mes_request.status_code)

            return Response({'error': 'Heading does not exist'}, status.HTTP_404_NOT_FOUND)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), status.HTTP_503_SERVICE_UNAVAILABLE)

    def patch(self, request, head_uuid, mes_uuid):
        self.info(request, f'get heading {head_uuid}')
        user_uuid = self.getUserUUID(request)
        token = request.auth.get('token')
        try:
            get_request = requests.get(
                f"{self.URL['heading']}/heading/{head_uuid}/", headers={'Authorization': f'Bearer {token}'})
            self.send_task('GET HEADING', user_uuid, after=get_request.json())

            if get_request.status_code >= 200 and get_request.status_code < 300:
                request.data['head_uuid'] = head_uuid
                patch_mes_request = requests.patch(
                    f"{self.URL['message']}/message/{mes_uuid}/", request.data, headers={'Authorization': f'Bearer {token}'})
                self.send_task('PATCH MESSAGE', user_uuid,
                               after=patch_mes_request.json())

                return Response(patch_mes_request.json(), patch_mes_request.status_code)

            return Response({'error': 'Heading does not exist'}, status.HTTP_404_NOT_FOUND)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), status.HTTP_503_SERVICE_UNAVAILABLE)

    def delete(self, request, head_uuid, mes_uuid):
        self.info(request, f'get heading {head_uuid}')
        user_uuid = self.getUserUUID(request)
        token = request.auth.get('token')
        try:
            get_request = requests.get(
                f"{self.URL['heading']}/heading/{head_uuid}/", headers={'Authorization': f'Bearer {token}'})
            self.send_task('GET HEADING', user_uuid, after=get_request.json())

            if get_request.status_code >= 200 and get_request.status_code < 300:
                get_mes_request = requests.delete(
                    f"{self.URL['message']}/message/{mes_uuid}/", headers={'Authorization': f'Bearer {token}'})
                self.send_task('DELETE MESSAGE', user_uuid)

                return Response(get_mes_request.json(), get_mes_request.status_code)

            return Response({'error': 'Heading does not exist'}, status.HTTP_404_NOT_FOUND)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), status.HTTP_503_SERVICE_UNAVAILABLE)
