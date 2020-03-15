from rest_framework import serializers

from .models import MessageModel

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        fields = ['uuid', 'head_uuid', 'body', 'parent', 'file', 'image']