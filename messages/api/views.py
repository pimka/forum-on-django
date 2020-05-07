from logging import getLogger

from celery import Celery
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from celery_queue.config import Config

from .auth import TokenAuth, TokenOAuth2
from .models import MessageModel
from .permissions import IsAuthenticate, IsOwner
from .serializers import MessageSerializer


class BaseView(APIView):
    celery = Celery()
    task_name = 'task.statistic.message'
    logger = getLogger('auth')
    __format = '{method} | {content_type} | {message}'

    def __init__(self, **kwargs):
        self.celery.config_from_object(Config)
        super().__init__(**kwargs)

    def send_task(self, operation, user_uuid=None, before=None, after=None):
        self.celery.send_task(self.task_name, [user_uuid, operation, before, after])

    def exception(self, request, message):
        self.logger.exception(self.__format.format(
            method = request.method,
            content_type = request.content_type,
            message = message
        ))

    def info(self, request, message):
        self.logger.info(self.__format.format(
            method = request.method,
            content_type = request.content_type,
            message = message
        ))

class MessageBaseOperations(BaseView):
    def get(self, request):
        self.info(request, 'getting all messages to heading')
        head = request.query_params.get('heading')

        if head:
            messages = MessageModel.objects.filter(head_uuid=head)
        else:
            messages = MessageModel.objects.all()
        
        serializer = MessageSerializer(data=messages, many=True)
        serializer.is_valid()
        user_uuid = request.auth.get('uuid') if request.auth else ''
        self.send_task('GET MESSAGES', user_uuid, after=serializer.data)
        return Response(serializer.data)

    def post(self, request):
        self.info(request, 'adding new message')
        serializer = MessageSerializer(data=request.data)
        user_uuid = request.auth.get('uuid') if request.auth else ''
        if serializer.is_valid():
            serializer.save()
            self.send_task('POST MESSAGE', user_uuid, after=serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        self.exception(request, f'Invalid data ({serializer.errors})')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageAdvancedOperations(BaseView):
    authentication_classes = [TokenAuth, TokenOAuth2]
    permission_classes = [IsAuthenticate, IsOwner]

    def get_object(self, uuid):
        try:
            return MessageModel.objects.get(uuid=uuid)
        except MessageModel.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        self.info(request, f'get message {uuid}')
        message = self.get_object(uuid)
        serializer = MessageSerializer(message)
        user_uuid = request.auth.get('uuid') if request.auth else ''

        self.send_task('GET MESSAGE', user_uuid, after=serializer.data)
        return Response(serializer.data)

    def patch(self, request, uuid):
        self.info(request, f'changing message {uuid}')
        message = self.get_object(uuid)
        old_data = MessageSerializer(message)
        serializer = MessageSerializer(message, request.data, partial=True)
        user_uuid = request.auth.get('uuid') if request.auth else ''

        if serializer.is_valid():
            serializer.save()
            self.send_task('PATCH MESSAGE', user_uuid, old_data.data, serializer.data)
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

        self.exception(request, f'Invalid data ({serializer.errors})')
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        self.info(request, f'deleting message {uuid}')
        message = self.get_object(uuid)
        old_data = MessageSerializer(message)
        message.delete()
        user_uuid = request.auth.get('uuid') if request.auth else ''

        self.send_task('DELETE MESSAGE', user_uuid, before=old_data.data)
        return Response(status=status.HTTP_204_NO_CONTENT)
