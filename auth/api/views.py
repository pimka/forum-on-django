from logging import getLogger

from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView, Response

from .models import ServiceToken, UserToken, UserCredentialsModel
from .permissions import IsAuth
from .serializers import ServicesTokenSerializer, UserCredentialSerializer
from .token import AuthTokenAuth, ServicesTokenAuth, UserAuth
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication


class BaseView(APIView):
    logger = getLogger('auth')
    __format = '{method} | {content_type} | {message}'
    model = None
    serializer = None
    permission_classes = (IsAuth, )

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

    def get(self, request):
        self.info(request, f'check token {request.auth}')
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        self.info(request, f'request token')
        serializer = self.serializer(
            data=request.data, context={'request': request})
        serializer.is_valid()
        token = self.model.objects.create()
        return Response(data={'token': token.token}, status=status.HTTP_200_OK)


class ServicesTokenView(BaseView):
    model = ServiceToken
    serializer = ServicesTokenSerializer
    service = 'users'
    authentication_classes = (ServicesTokenAuth, )

    def get(self, request):
        self.info(request, f'check token {request.auth}')
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        self.info(request, 'request token')
        serializer = self.serializer(
            data=request.data, context={'request': request})
        serializer.is_valid()
        token = self.model.objects.create()
        return Response({'token': token.token}, status.HTTP_200_OK)


class UsersLoginView(BaseView):
    authentication_classes = (UserAuth, )
    model = UserToken

    def post(self, request):
        self.info(request, f'{request.user.username} request for token')
        token, created = self.model.objects.get_or_create(user=request.user)
        return Response({'token': token.token, 'uuid': request.user.uuid, 'is_superuser': request.user.is_superuser, 'is_staff': request.user.is_staff}, status.HTTP_200_OK)


class AuthTokenView(BaseView):
    authentication_classes = (AuthTokenAuth, )

    def get(self, request):
        self.info(request, f'check user {request.auth}')
        return Response(data={'uuid': request.auth.user.uuid, 'is_staff': request.auth.user.is_staff}, status=status.HTTP_200_OK)


class UsersBaseView(BaseView):
    model = UserCredentialsModel
    serializer = UserCredentialSerializer

    def post(self, request):
        self.info(request, 'Add user')
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        self.exception(request, f'Invalid data ({serializer.errors})')
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UsersAdvancedView(BaseView):
    model = UserCredentialsModel
    serializer = UserCredentialSerializer
    authentication_classes = (AuthTokenAuth, )

    def patch(self, request, uuid):
        self.info(request, f'Change user {uuid}')

        try:
            user = self.model.objects.get(uuid=uuid)
        except self.model.DoesNotExist:
            self.exception(f'User {uuid} not found')
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer(instance=user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED)

        self.exception(request, f'Invalid data for {uuid}')
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class OAuth2View(BaseView):
    authentication_classes = (OAuth2Authentication,)
    permission_classes = (IsAuth,)

    def get(self, request):
        self.info(request, f'get oauth token for {request.auth} user')
        return Response(data={'username': request.user.username, 'uuid': request.user.uuid, 'is_staff': request.user.is_staff}, status=status.HTTP_200_OK)
