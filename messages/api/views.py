from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MessageModel
from .serializers import MessageSerializer

class MessageBaseOperations(APIView):
    def get(self, request):
        messages = MessageModel.objects.all()
        serializer = MessageSerializer(data=messages, many=True)
        return Response(serializer.data)