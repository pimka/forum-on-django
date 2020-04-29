from rest_framework import serializers

from .models import HeadingModel, TagModel


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ['uuid', 'name']

class HeadingSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = HeadingModel
        fields = ['uuid', 'user_uuid', 'tags', 'header', 'body', 'views', 'created']
