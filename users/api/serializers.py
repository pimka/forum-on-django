import django.contrib.auth.password_validation as validators
from django.core import exceptions
from rest_framework import serializers

from .auth import send_credentials, update_credentials
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'uuid', 'username', 'is_moderate', 'password']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        credentials = {
            'username' : validated_data['username'],
            'password' : validated_data.get('password'),
            'uuid' : user.uuid
        }
        response, status = send_credentials(credentials)
        
        if status != 201:
            user.delete()
            raise serializers.ValidationError(response.get('error', str(response)))

        return user

    def update(self, instance, validated_data):
        credentials = dict()

        if validated_data.get('username'):
            username = validated_data.get('username')
            credentials['username'] = username
            instance.username = username

        if validated_data.get('is_moderate'):
            moder = validated_data.get('is_moderate') and instance.is_stuff
            instance.is_moderate = moder

        if validated_data.get('password'):
            password = validated_data.get('password')
            credentials['password'] = password
            instance.set_password(password)

        if credentials:
            response, status = update_credentials(instance.uuid, credentials)
            if status != 200:
                raise serializers.ValidationError(response.get('error', ''))

        instance.save()
        return instance
