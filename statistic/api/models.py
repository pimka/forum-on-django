from django.db import models
from jsonfield import JSONField


class StatisicModel(models.Model):
    user_uuid = models.UUIDField(null=False, unique=False, editable=False)
    datetime_operation = models.DateTimeField(auto_now=True)
    operation = models.CharField(unique=False, null=False, editable=False)
    before_changes = JSONField(null=True, blank=True)
    after_changes = JSONField(null=True, blank=True)
