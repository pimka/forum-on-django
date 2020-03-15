from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import HeadingModel, TagModel
from .serializers import HeadingSerializer, TagSerializer

class TagBaseOperations(APIView):
    def get(self, request):
        tags = TagModel.objects.all()
        serializer = TagSerializer(data=tags, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HeadingBaseOperations(APIView):
    def get(self, request):
        heads = HeadingModel.object.all()
        serializer = HeadingSerializer(data=heads, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HeadingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagAdvancedOperations(APIView):
    def get_object(self, uuid):
        try:
            return TagModel.objects.get(uuid=uuid)
        except TagModel.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        tag = self.get_object(uuid)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def patch(self, request, uuid):
        tag = self.get_object(uuid)
        serializer = TagSerializer(tag, request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        tag = self.get_object(uuid)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class HeadingAdvancedOperations(APIView):
    def get_object(self, uuid):
        try:
            return HeadingModel.objects.get(uuid=uuid)
        except HeadingModel.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        head = self.get_object(uuid)
        serializer = HeadingSerializer(head)
        return Response(serializer.data)

    def patch(self, request, uuid):
        head = self.get_object(uuid)
        serializer = HeadingSerializer(head, request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        head = self.get_object(uuid)
        head.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)