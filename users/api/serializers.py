import django.contrib.auth.password_validation as validators
from django.core import exceptions
from rest_framework import serializers

from api.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'uuid', 'password', 'username', 'is_moderate']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)

        if validated_data.get('password'):
            new_password = validated_data.get('password')
            instance.set_password(new_password)

        if validated_data.get('is_moderate'):
            moder = validated_data.get('is_moderate') and instance.is_stuff
            instance.is_moderate = moder

        instance.save()
        return instance