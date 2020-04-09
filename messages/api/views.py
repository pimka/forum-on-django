from logging import getLogger

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .auth import TokenAuth
from .models import MessageModel
from .permissions import IsAuthenticate, IsOwner
from .serializers import MessageSerializer


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

class MessageBaseOperations(BaseView):
    def get(self, request):
        self.info(request, 'getting all messages')
        messages = MessageModel.objects.all()
        serializer = MessageSerializer(data=messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        self.info(request, 'adding new message')
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        self.exception(request, f'Invalid data ({serializer.errors})')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageAdvancedOperations(BaseView):
    authentication_classes = [TokenAuth]
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
        return Response(serializer.data)

    def patch(self, request, uuid):
        self.info(request, f'changing message {uuid}')
        message = self.get_object(uuid)
        serializer = MessageSerializer(message, request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

        self.exception(request, f'Invalid data ({serializer.errors})')
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        self.info(request, f'deleting message {uuid}')
        message = self.get_object(uuid)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)