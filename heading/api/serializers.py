from rest_framework import serializers

from .models import HeadingModel, TagModel
import json


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ['uuid', 'name']

class HeadingSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True,slug_field='uuid', queryset=TagModel.objects.all())

    class Meta:
        model = HeadingModel
        fields = ['uuid', 'user_uuid', 'tags', 'header', 'body', 'views', 'created']
