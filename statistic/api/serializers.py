from rest_framework import serializers

from .models import StatisicModel


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatisicModel
        fields = '__all__'