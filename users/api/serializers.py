import django.contrib.auth.password_validation as validators
from django.core import exceptions
from rest_framework import serializers

from api.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'uuid', 'username', 'is_moderate']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)

        if validated_data.get('is_moderate'):
            moder = validated_data.get('is_moderate') and instance.is_stuff
            instance.is_moderate = moder

        instance.save()
        return instance