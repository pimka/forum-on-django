from rest_framework import serializers

from .models import StatisicModel


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatisicModel
        fields = ['user_uuid', 'operation', 'datetime_operation', 'before_changes', 'after_changes']