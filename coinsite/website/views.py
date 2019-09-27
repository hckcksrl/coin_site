from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
import json
import requests
from . import serializers
from . import models
from collections import OrderedDict

NotFound = Response(status=status.HTTP_404_NOT_FOUND)

with open('/Users/hckcksrl/Desktop/study/coinsite/coinsite/website/config.json', 'r') as f:
    config = json.load(f)


class CoinOne(APIView):

    def get_coin(self, name):
        api = f'https://api.coinone.co.kr/ticker?currency={name}'
        data = requests.get(api)
        return data.json()

    def get(self, request:Request):

        data = config["coinone"]
        coin_list = list(data.keys())
        coin_serial = list()
        for name in coin_list:
            coin = self.get_coin(name=name)
            price = coin["last"]
            currency = coin["currency"].upper()
            high = coin["high"]
            low = coin["low"]
            volume = coin["low"]
            coin_model = models.Coin(price=price, currency=currency, high=high, low=low, volume=volume)
            coin_serial.append(coin_model)


        serializer = serializers.CoinSerializer(coin_serial, many=True)

        return Response(status=status.HTTP_200_OK,data=serializer.data)


class UpBit(APIView):

    def get_coin(self, name):
        name = name.upper()
        if not name.startswith('KRW-'):
            name = f'KRW-{name}'
        api = f'https://api.upbit.com/v1/ticker?markets={name}'
        data = requests.get(api)

        if data.status_code == 404:
            return False
        return data.json()

    def get(self, request:Request):

        data = config["upbit"]
        coin_list = list(data.keys())
        coin_serial = list()
        for name in coin_list:
            coin = self.get_coin(name=name)
            price = float(coin[0]["trade_price"])
            currency = name
            high = float(coin[0]["high_price"])
            low = float(coin[0]["low_price"])
            volume = float(coin[0]["acc_trade_volume"])
            model = models.Coin(price=price, currency=currency, high=high, low=low, volume=volume)
            coin_serial.append(model)
        serializer = serializers.CoinSerializer(coin_serial, many=True)

        return Response(status=status.HTTP_200_OK,data=serializer.data)

class Bithumb(APIView):

    def get_coin(self, name):
        api = f'https://api.bithumb.com/public/ticker/{name}'
        data = requests.get(api)
        if data.status_code == 400:
            return False
        return data.json()

    def get(self, request:Request):

        data = config["bithumb"]
        coin_list = list(data.keys())
        coin_serial = list()
        for name in coin_list:
            coin = self.get_coin(name=name)
            price = float(coin['data']["closing_price"])
            currency = name
            high = float(coin['data']["max_price"])
            low = float(coin['data']["min_price"])
            volume = float(coin['data']["units_traded_24H"])
            coin_model = models.Coin(price=price, currency=currency, high=high, low=low, volume=volume)
            coin_serial.append(coin_model)

        serializer = serializers.CoinSerializer(coin_serial, many=True)

        return Response(status=status.HTTP_200_OK,data=serializer.data)


class KorBit(APIView):

    def get_coin(self, name):
        coin_name = f'{name.lower()}_krw'
        api = f'https://api.korbit.co.kr/v1/ticker/detailed?currency_pair={coin_name}'
        data = requests.get(api)
        if data.status_code == 400:
            return False
        return data.json()

    def get(self, request: Request):

        data = config["korbit"]
        coin_list = list(data.keys())
        coin_serial = list()
        for name in coin_list:
            coin = self.get_coin(name=name)
            price = float(coin["last"])
            currency = name
            high = float(coin["high"])
            low = float(coin["low"])
            volume = float(coin["volume"])
            coin_model = models.Coin(price=price, currency=currency, high=high, low=low, volume=volume)
            coin_serial.append(coin_model)

        serializer = serializers.CoinSerializer(coin_serial, many=True)

        return Response(status=status.HTTP_200_OK,data=serializer.data)


# Create your views here.
