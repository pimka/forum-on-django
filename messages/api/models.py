import uuid

from django.db import models

class MessageModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    head_uuid = models.UUIDField(null=False)
    body = models.TextField(null=False)
    parent = models.UUIDField(null=True)
    file = models.FileField(null=True)
    image = models.ImageField(null=True)
    user_uuid = models.UUIDField(null=False, unique=False)
    created = models.DateTimeField(auto_now_add=True)