from logging import getLogger

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .auth import TokenAuth
from .models import HeadingModel, TagModel
from .permissions import IsAuthenticate, IsOwner
from .serializers import HeadingSerializer, TagSerializer
import celery_queue.tasks as tasks

URL = {
    'statistic' : ''
}

class BaseView(APIView):
    logger = getLogger('auth')
    __format = '{method} | {content_type} | {message}'

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

    def json_for_statistic(self, request, operation, before=None, after=None):
        return {
            'user_uuid' : request.auth.get('uuid') if bool(request.auth) else '',
            'operation' : operation,
            'before_changes' : before,
            'after_changes' : after
        }

class TagBaseOperations(BaseView):
    authentication_classes = [TokenAuth]
    permission_classes = [IsAuthenticate]

    def get(self, request):
        self.info(request, 'getting all tags')
        tags = TagModel.objects.all()
        serializer = TagSerializer(data=tags, many=True)

        tasks.post.delay(URL['statistic'], self.json_for_statistic(request, 'GET TAGS'))
        return Response(serializer.data)

    def post(self, request):
        self.info(request, 'adding new tag')
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            tasks.post.delay(URL['statistic'], self.json_for_statistic(request, 'POST TAG'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        self.exception(request, f'Invalid data ({serializer.errors})')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HeadingBaseOperations(BaseView):
    def get(self, request):
        self.info(request, 'getting all headings')
        heads = HeadingModel.object.all()
        serializer = HeadingSerializer(data=heads, many=True)

        tasks.post.delay(URL['statistic'], self.json_for_statistic(request, 'GET HEADINGS'))
        return Response(serializer.data)

    def post(self, request):
        self.info(request, 'adding new heading')
        serializer = HeadingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            tasks.post.delay(URL['statistic'], self.json_for_statistic(request, 'POST HEADING'))
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

        tasks.post.delay(URL['statistic'], self.json_for_statistic(request, 'GET TAG'))
        return Response(serializer.data)

    def patch(self, request, uuid):
        self.info(request, f'changing tag {uuid}')
        tag = self.get_object(uuid)
        serializer = TagSerializer(tag, request.data)

        if serializer.is_valid():
            serializer.save()
            tasks.post.delay(
                URL['statistic'], 
                self.json_for_statistic(request, 'PATCH TAG', request.data, serializer.data)
            )
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

        self.exception(request, f'Invalid data ({serializer.errors})')
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        self.info(request, f'deleting tag {uuid}')
        tag = self.get_object(uuid)
        tag.delete()

        tasks.post.delay(URL['statistic'], self.json_for_statistic(request, 'DELETE TAG'))
        return Response(status=status.HTTP_204_NO_CONTENT)

class HeadingAdvancedOperations(BaseView):
    authentication_classes = [TokenAuth]
    permission_classes = [IsAuthenticate, IsOwner]

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

        serializer = HeadingSerializer(head)
        tasks.post.delay(URL['statistic'], self.json_for_statistic(request, 'GET HEADING'))
        return Response(serializer.data)

    def patch(self, request, uuid):
        self.info(request, f'changing heading {uuid}')
        head = self.get_object(uuid)
        serializer = HeadingSerializer(head, request.data)

        if serializer.is_valid():
            serializer.save()
            tasks.post.delay(URL['statistic'], self.json_for_statistic(request, 'PATCH HEADING'))
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

        self.exception(request, f'Invalid data ({serializer.errors})')
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        self.info(request, f'deleting heading {uuid}')
        head = self.get_object(uuid)
        head.delete()
        tasks.post.delay(URL['statistic'], self.json_for_statistic(request, 'DELETE HEADING'))
        return Response(status=status.HTTP_204_NO_CONTENT)
