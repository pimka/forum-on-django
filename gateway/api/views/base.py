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
           'message': 'http://localhost:8082', 'tag': 'http://localhost:8083', 'user': 'http://localhost:8081'}

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