from logging import getLogger

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .auth import TokenAuth, TokenOAuth2
from .models import User
from .permissions import IsAuthenticate, IsOwner
from .serializers import UserSerializer


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


class UserBaseOperations(BaseView):
    permission_classes = [IsAuthenticate]
    authentication_classes = [TokenAuth, TokenOAuth2]

    def post(self, request):
        self.info(request, 'Add user')
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        self.exception(request, f'Invalid data ({serializer.errors})')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUserView(BaseView):
    def get(self, request, uuid, *args, **kwargs):
        try:
            self.info(request, f'Get user {uuid}')
            user = User.objects.get(uuid=uuid)
        except User.DoesNotExist:
            self.exception(request, f'User {uuid} not founded')
            raise Http404

        self.check_object_permissions(request, user)

        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserAdvancedOperations(BaseView):
    permission_classes = [IsOwner, ]

    def patch(self, request, uuid):
        try:
            self.info(request, f'Change user {uuid}')
            user = User.objects.get(uuid=uuid)
        except User.DoesNotExist:
            self.exception(request, f'User {uuid} not founded')
            raise Http404
        
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

        self.exception(request, f'Invalid data ({serializer.errors})')
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        self.info(request, f'Delete user')
        if request.user is None:
            self.exception(request, 'Invalid credentials')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
