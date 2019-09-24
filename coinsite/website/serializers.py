from rest_framework import serializers
from . import models


class CoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Coin
        field = (
            'name',
            'price',
            'high',
            'low',
            'volume'
        )

