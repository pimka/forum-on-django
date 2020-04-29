import uuid

from django.db import models
import binascii, os

class TagModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

class HeadingModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user_uuid = models.UUIDField(null=False, unique=False)
    tags = models.ManyToManyField(TagModel)
    header = models.CharField(max_length=250, null=False)
    body = models.TextField(null=False)
    views = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)