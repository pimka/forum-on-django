import binascii
import os

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserCredentialsModel(AbstractUser):
    uuid = models.UUIDField(unique=True, null=False, editable=False)

class TokenBaseModel(models.Model):
    class Meta:
        abstract = True

    token = models.CharField(verbose_name='Token', unique=True, max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = binascii.hexlify(os.urandom(20)).decode(0)
        return super().save(*args, **kwargs)

class UserToken(TokenBaseModel):
    user = models.OneToOneField(to=UserCredentialsModel, on_delete=models.CASCADE)

class ServiceToken(TokenBaseModel):
    pass
