from rest_framework import serializers
from . import models


class CoinSerializer(serializers.Serializer):

    price = serializers.FloatField()
    currency = serializers.CharField()
    high = serializers.FloatField()
    low = serializers.FloatField()
    volume = serializers.FloatField()
    korean = serializers.CharField()
    rate = serializers.FloatField()
