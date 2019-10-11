from rest_framework import serializers
from . import models


class CoinSerializer(serializers.ModelSerializer):

    price = serializers.FloatField()
    currency = serializers.CharField()
    high = serializers.FloatField()
    low = serializers.FloatField()
    volume = serializers.FloatField()
    korean = serializers.CharField()
    rate = serializers.FloatField()

    class Meta:
        model = models.Coin
        fields = (
            'currency',
            'price',
            'high',
            'low',
            'volume',
            'korean',
            'rate'
        )

