from logging import getLogger

import requests
from celery import Celery
from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from celery_queue.config import Config


# Добавить перемещение header и добавление в очередь
class BaseView(APIView):
    celery = Celery()
    task_name = 'task.statistic.gateway'
    logger = getLogger('gateway')
    __format = '{method} | {content_type} | {message}'
    URL = {'heading': 'http://localhost:8083',
           'message': 'http://localhost:8082', 'tag': 'http://localhost:8082', 'user': 'http://localhost:8081'}

    def __init__(self, **kwargs):
        self.celery.config_from_object(Config)
        super().__init__(**kwargs)

    def send_task(self, operation, user_uuid=None, before=None, after=None):
        self.celery.send_task(
            self.task_name, [user_uuid, operation, before, after])

    def exception(self, request, message):
        self.logger.exception(self.__format.format(
            method=request.method,
            content_type=request.content_type,
            message=message
        ))

    def info(self, request, message):
        self.logger.info(self.__format.format(
            method=request.method,
            content_type=request.content_type,
            message=message
        ))

    def getUserUUID(self, request):
        return request.auth.get('uuid') if request.auth else ''


class HeadingsView(BaseView):
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

    def post(self, request):
        self.info(request, 'add new heading')
        user_uuid = self.getUserUUID(request)
        try:
            post_request = requests.post(
                self.URL['heading']+'/headings_add/', request.data)
            self.send_task('POST HEADING', user_uuid,
                           after=post_request.json())
            return Response(post_request.json(), post_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), post_request.status_code)


class ConcreteHeadingView(BaseView):
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

    def patch(self, request, head_uuid):
        self.info(request, f'patch heading {head_uuid}')
        user_uuid = self.getUserUUID(request)
        try:
            patch_request = requests.patch(
                f"{self.URL['heading']}/headings/{head_uuid}/", request.data)
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

    def post(self, request):
        self.info(request, 'add new tag')
        user_uuid = self.getUserUUID(request)
        try:
            post_request = requests.post(
                self.URL['tag']+'/tags_add/', request.data)
            self.send_task('POST TAG', user_uuid,
                           after=post_request.json())
            return Response(post_request.json(), post_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), post_request.status_code)


class ConcreteTagView(BaseView):
    def get(self, request, tag_uuid):
        self.info(request, f'get tag {tag_uuid}')
        user_uuid = self.getUserUUID(request)
        try:
            get_request = requests.get(
                f"{self.URL['tag']}/get_tags/{tag_uuid}/")
            self.send_task('GET TAG', user_uuid, after=get_request.json())
            return Response(get_request.json(), get_request.status_code)
        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), get_request.status_code)

    def patch(self, request, tag_uuid):
        self.info(request, f'patch tag {tag_uuid}')
        user_uuid = self.getUserUUID(request)
        try:
            patch_request = requests.patch(
                f"{self.URL['tag']}/tags/{tag_uuid}/", request.data)
            self.send_task('PATCH TAG', user_uuid,
                           after=patch_request.json())
            return Response(patch_request.json(), patch_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), patch_request.status_code)

    def delete(self, request, tag_uuid):
        self.info(request, f'deleting tag {tag_uuid}')
        user_uuid = self.getUserUUID(request)
        try:
            delete_request = requests.delete(
                f"{self.URL['tag']}/tags/{tag_uuid}/")
            self.send_task('DELETE TAG', user_uuid)

            return Response(status=delete_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), status.HTTP_503_SERVICE_UNAVAILABLE)


class MessagesView(BaseView):
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

    def post(self, request):
        self.info(request, 'add new message')
        user_uuid = self.getUserUUID(request)
        try:
            post_request = requests.post(
                self.URL['message']+'/messages/', request.data)
            self.send_task('POST MESSAGE', user_uuid,
                           after=post_request.json())
            return Response(post_request.json(), post_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), post_request.status_code)


class ConcreteMessageView(BaseView):
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

    def patch(self, request, mes_uuid):
        self.info(request, f'patch message {mes_uuid}')
        user_uuid = self.getUserUUID(request)
        try:
            patch_request = requests.patch(
                f"{self.URL['message']}/messages/{mes_uuid}/", request.data)
            self.send_task('PATCH MESSAGE', user_uuid,
                           after=patch_request.json())
            return Response(patch_request.json(), patch_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), patch_request.status_code)

    def delete(self, request, mes_uuid):
        self.info(request, f'deleting message {mes_uuid}')
        user_uuid = self.getUserUUID(request)
        try:
            delete_request = requests.delete(
                f"{self.URL['message']}/messages/{mes_uuid}/")
            self.send_task('DELETE MESSAGE', user_uuid)

            return Response(status=delete_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), status.HTTP_503_SERVICE_UNAVAILABLE)


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


class ConcreteUserView(BaseView):
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

    def patch(self, request, user_uuid):
        self.info(request, f'patch user {user_uuid}')
        user_uuid = self.getUserUUID(request)
        try:
            patch_request = requests.patch(
                f"{self.URL['user']}/user/{user_uuid}/", request.data)
            self.send_task('PATCH USER', user_uuid,
                           after=patch_request.json())
            return Response(patch_request.json(), patch_request.status_code)

        except requests.RequestException as err:
            self.exception(request, str(err))
            return Response(str(err), patch_request.status_code)

