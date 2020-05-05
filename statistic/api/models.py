from django.db import models
from jsonfield import JSONField


class StatisicModel(models.Model):
    user_uuid = models.UUIDField(null=True, unique=False)
    datetime_operation = models.DateTimeField(auto_now=True)
    operation = models.CharField(unique=False, blank=False, max_length=50)
    before_changes = JSONField(null=True, blank=True)
    after_changes = JSONField(null=True, blank=True)
