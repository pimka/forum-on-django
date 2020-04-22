import django.contrib.auth.password_validation as validators
from django.core import exceptions
from rest_framework import serializers

from .auth import send_credentials, update_credentials
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'username', 'is_staff', 'password']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        credentials = {
            'username' : validated_data['username'],
            'password' : validated_data.get('password'),
            'uuid' : user.uuid,
            'is_staff' : user.is_staff
        }
        response, status = send_credentials(credentials)
        
        if status != 201:
            user.delete()
            raise serializers.ValidationError(response.get('error', str(response)))

        return user

    def update(self, instance, validated_data):
        credentials = dict()

        if validated_data.get('username'):
            username = validated_data.pop('username')
            credentials['username'] = username
            instance.username = username

        if validated_data.get('is_staff'):
            is_staff = validated_data.pop('is_staff')
            credentials['is_staff'] = is_staff
            instance.is_moderate = is_staff

        if validated_data.get('password'):
            password = validated_data.pop('password')
            credentials['password'] = password
            instance.set_password(password)

        if credentials:
            response, status = update_credentials(instance.uuid, credentials)
            if status != 200:
                raise serializers.ValidationError(response.get('error', ''))

        instance.save()
        return instance
