from logging import getLogger

from celery import Celery
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from celery_queue.config import Config

from .auth import TokenAuth
from .models import HeadingModel, TagModel
from .permissions import IsAuthenticate, IsOwner
from .serializers import HeadingSerializer, TagSerializer


class BaseView(APIView):
    celery = Celery()
    task_name = 'task.statistic.heading'
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

class GetTagsView(BaseView):

    def get(self, request):
        self.info(request, 'getting all tags')
        tags = TagModel.objects.all()
        serializer = TagSerializer(instance=tags, many=True)

        user_uuid = ''#request.user.auth.get('uuid')

        self.send_task('GET TAGS', user_uuid, after=serializer.data)
        return Response(serializer.data)

class TagBaseOperations(BaseView):
    authentication_classes = [TokenAuth]
    permission_classes = [IsAuthenticate]

    def post(self, request):
        self.info(request, 'adding new tag')
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.send_task('POST TAG', request.auth.get('uuid'), after=serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        self.exception(request, f'Invalid data ({serializer.errors})')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetHeadingsView(BaseView):
    def get(self, request):
        self.info(request, 'getting all headings')
        heads = HeadingModel.objects.all()
        serializer = HeadingSerializer(data=heads, many=True)
        serializer.is_valid()

        user_uuid = ''#request.auth.get('uuid')

        self.send_task('GET HEADINGS', user_uuid, after=serializer.data)
        return Response(serializer.data)

class HeadingBaseOperations(BaseView):
    authentication_classes = [TokenAuth]
    permission_classes = [IsAuthenticate]

    def post(self, request):
        self.info(request, 'adding new heading')
        serializer = HeadingSerializer(data=request.data)
        user_uuid = ''#request.auth.get('uuid')
        if serializer.is_valid():
            serializer.save()
            self.send_task('POST HEADING', user_uuid, after=serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        self.exception(request, f'Invalid data ({serializer.errors})')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagAdvancedOperations(BaseView):
    authentication_classes = [TokenAuth]
    permission_classes = [IsAuthenticate]

    def get_object(self, uuid):
        try:
            return TagModel.objects.get(uuid=uuid)
        except TagModel.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        self.info(request, f'get tag {uuid}')
        tag = self.get_object(uuid)
        serializer = TagSerializer(tag)

        self.send_task('GET TAG', request.auth.get('uuid'), after=serializer.data)
        return Response(serializer.data)

    def patch(self, request, uuid):
        self.info(request, f'changing tag {uuid}')
        tag = self.get_object(uuid)
        old_data = TagSerializer(tag)
        serializer = TagSerializer(tag, request.data)

        if serializer.is_valid():
            serializer.save()
            self.send_task('PATCH TAG', request.auth.get('uuid'), old_data.data, serializer.data)
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

        self.exception(request, f'Invalid data ({serializer.errors})')
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        self.info(request, f'deleting tag {uuid}')
        tag = self.get_object(uuid)
        old_data = TagSerializer(tag)
        tag.delete()

        self.send_task('DELETE TAG', request.auth.get('uuid'), before=old_data.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetConcreteHeadingView(BaseView):
    def get_object(self, uuid):
        try:
            return HeadingModel.objects.get(uuid=uuid)
        except HeadingModel.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        self.info(request, f'get heading {uuid}')
        head = self.get_object(uuid)
        head.views += 1
        head.save()
        user_uuid = ''#request.auth.get('uuid')

        serializer = HeadingSerializer(head)
        self.send_task('GET HEADING', user_uuid, after=serializer.data)
        return Response(serializer.data)

class HeadingAdvancedOperations(BaseView):
    authentication_classes = [TokenAuth]
    permission_classes = [IsAuthenticate, IsOwner]

    def get_object(self, uuid):
        try:
            return HeadingModel.objects.get(uuid=uuid)
        except HeadingModel.DoesNotExist:
            raise Http404

    def patch(self, request, uuid):
        self.info(request, f'changing heading {uuid}')
        head = self.get_object(uuid)
        old_data = HeadingSerializer(head)
        serializer = HeadingSerializer(head, request.data)

        if serializer.is_valid():
            serializer.save()
            self.send_task('PATCH HEADING', request.auth.get('uuid'), old_data.data, serializer.data)
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

        self.exception(request, f'Invalid data ({serializer.errors})')
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        self.info(request, f'deleting heading {uuid}')
        head = self.get_object(uuid)
        old_data = HeadingSerializer(head)
        head.delete()

        self.send_task('DELETE HEADING', request.auth.get('uuid'), before=old_data.data)
        return Response(status=status.HTTP_204_NO_CONTENT)
