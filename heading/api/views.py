from logging import getLogger

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import HeadingModel, TagModel
from .serializers import HeadingSerializer, TagSerializer


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

class TagBaseOperations(BaseView):
    def get(self, request):
        self.info(request, 'getting all tags')
        tags = TagModel.objects.all()
        serializer = TagSerializer(data=tags, many=True)
        return Response(serializer.data)

    def post(self, request):
        self.info(request, 'adding new tag')
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        self.exception(request, f'Invalid data ({serializer.errors})')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HeadingBaseOperations(BaseView):
    def get(self, request):
        self.info(request, 'getting all headings')
        heads = HeadingModel.object.all()
        serializer = HeadingSerializer(data=heads, many=True)
        return Response(serializer.data)

    def post(self, request):
        self.info(request, 'adding new heading')
        serializer = HeadingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        self.exception(request, f'Invalid data ({serializer.errors})')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagAdvancedOperations(BaseView):
    def get_object(self, uuid):
        try:
            return TagModel.objects.get(uuid=uuid)
        except TagModel.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        self.info(request, f'get tag {uuid}')
        tag = self.get_object(uuid)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def patch(self, request, uuid):
        self.info(request, f'changing tag {uuid}')
        tag = self.get_object(uuid)
        serializer = TagSerializer(tag, request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

        self.exception(request, f'Invalid data ({serializer.errors})')
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        self.info(request, f'deleting tag {uuid}')
        tag = self.get_object(uuid)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class HeadingAdvancedOperations(BaseView):
    

    def get_object(self, uuid):
        try:
            return HeadingModel.objects.get(uuid=uuid)
        except HeadingModel.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        self.info(request, f'get heading {uuid}')
        head = self.get_object(uuid)
        serializer = HeadingSerializer(head)
        return Response(serializer.data)

    def patch(self, request, uuid):
        self.info(request, f'changing heading {uuid}')
        head = self.get_object(uuid)
        serializer = HeadingSerializer(head, request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

        self.exception(request, f'Invalid data ({serializer.errors})')
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        self.info(request, f'deleting heading {uuid}')
        head = self.get_object(uuid)
        head.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
