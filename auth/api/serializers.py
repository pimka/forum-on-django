from rest_framework import serializers

from auth.auth.settings import SERVICES_CREDENTIALS

from .models import UserCredentialsModel


class UserCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCredentialsModel
        fields = ['uuid', 'password', 'username']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserCredentialsModel.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)

        if validated_data.get('password'):
            new_password = validated_data.get('password')
            instance.set_password(new_password)

        instance.save()
        return instance

class TokenBaseSerializer(serializers.Serializer):
    id_service = serializers.CharField()
    secret = serializers.CharField()

    SERVICES_CREDENTIALS = dict()

    def validate(self, attrs):
        id_s = attrs.get('id_service')
        scrt = attrs.get('secret')

        if id_s and scrt:
            is_valid = False
            for sc in self.SERVICES_CREDENTIALS.items():
                if sc['id'] == id_s and sc['secret'] == scrt:
                    is_valid = True
                    break
            if not is_valid:
                raise serializers.ValidationError('Invalid credentials', code='authorization')
        else:
            raise serializers.ValidationError('Credentials not found', code='authorization')

        return attrs

class ServicesTokenSerializer(TokenBaseSerializer):
    SERVICES_CREDENTIALS = SERVICES_CREDENTIALS
