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
            korean = coin["korean"]
            rate = coin["rate"]
            coin_model = models.Coin(price=price, currency=currency, high=high, low=low, volume=volume, korean=korean, rate=rate)
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
            korean = coin["korean"]
            rate = coin["rate"]
            coin_model = models.Coin(price=price, currency=currency, high=high, low=low, volume=volume, korean=korean, rate=rate)
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
            korean = coin["korean"]
            rate = coin["rate"]
            coin_model = models.Coin(price=price, currency=currency, high=high, low=low, volume=volume, korean=korean, rate=rate)
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
            korean = coin["korean"]
            rate = coin["rate"]
            coin_model = models.Coin(price=price, currency=currency, high=high, low=low, volume=volume, korean=korean, rate=rate)
            coin_serial.append(coin_model)

        serializer = serializers.CoinSerializer(coin_serial, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class Search(APIView):

    def is_exist(self, name, data, exchange):
        coin = json.loads(data)
        coin_name = name.upper()
        for i in list(coin.keys()):
            if i == coin_name:
                coin[i]["exchange"] = exchange
                return coin[i]

        return False



    def get(self, request: Request):
        name = request.GET["name"]

        bithumb_data = cache.get('bithumb')
        coinone_data = cache.get('coinone')
        upbit_data = cache.get('upbit')
        korbit_data = cache.get('korbit')

        data_list = [bithumb_data, upbit_data, coinone_data, korbit_data]
        exchange_list = ['빗썸', '업비트', '코인원', '코빗']
        result_list = list()

        for (data,exchange) in zip(data_list,exchange_list):
            result = self.is_exist(name, data, exchange)
            if result != False:
                result_list.append(result)

        return Response(status=status.HTTP_200_OK,data=result_list)

