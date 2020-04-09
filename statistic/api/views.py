from logging import getLogger

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import StatisicModel
from .serializers import StatisticSerializer


class StatisticOperations(APIView):
    logger = getLogger('auth')
    __format = '{method} | {content_type} | {message}'

    def info(self, request, message):
        self.logger.info(self.__format.format(
            method = request.method,
            content_type = request.content_type,
            message = message
        ))

    def post(self, request):
        self.info(request, 'adding stats')
        serializer = StatisticSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
