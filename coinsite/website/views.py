from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
from django.core.cache import cache
import json
import requests
from . import serializers
from . import models

class CoinOne(APIView):

    def get(self, request:Request):

        coin_string_data = cache.get('coinone')
        coin_data_dict = json.loads(coin_string_data)
        coin_data = list(coin_data_dict.values())
        coin_serial = list()
        for coin in coin_data:
            price = coin["price"]
            currency = coin["currency"]
            high = coin["high"]
            low = coin["low"]
            volume = coin["volume"]
            coin_model = models.Coin(price=price, currency=currency, high=high, low=low, volume=volume)
            coin_serial.append(coin_model)

        serializer = serializers.CoinSerializer(coin_serial, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UpBit(APIView):

    def get(self, request: Request):
        coin_string_data = cache.get('upbit')
        coin_data_dict = json.loads(coin_string_data)
        coin_data = list(coin_data_dict.values())
        coin_serial = list()
        for coin in coin_data:
            price = coin["price"]
            currency = coin["currency"]
            high = coin["high"]
            low = coin["low"]
            volume = coin["volume"]
            coin_model = models.Coin(price=price, currency=currency, high=high, low=low, volume=volume)
            coin_serial.append(coin_model)

        serializer = serializers.CoinSerializer(coin_serial, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class Bithumb(APIView):

    def get(self, request: Request):
        coin_string_data = cache.get('bithumb')
        coin_data_dict = json.loads(coin_string_data)
        coin_data = list(coin_data_dict.values())
        coin_serial = list()
        for coin in coin_data:
            price = coin["price"]
            currency = coin["currency"]
            high = coin["high"]
            low = coin["low"]
            volume = coin["volume"]
            coin_model = models.Coin(price=price, currency=currency, high=high, low=low, volume=volume)
            coin_serial.append(coin_model)

        serializer = serializers.CoinSerializer(coin_serial, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class KorBit(APIView):

    def get(self, request: Request):
        coin_string_data = cache.get('korbit')
        coin_data_dict = json.loads(coin_string_data)
        coin_data = list(coin_data_dict.values())
        coin_serial = list()
        for coin in coin_data:
            price = coin["price"]
            currency = coin["currency"]
            high = coin["high"]
            low = coin["low"]
            volume = coin["volume"]
            coin_model = models.Coin(price=price, currency=currency, high=high, low=low, volume=volume)
            coin_serial.append(coin_model)

        serializer = serializers.CoinSerializer(coin_serial, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

# Create your views here.
