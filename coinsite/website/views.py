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

    def get_coin(self):
        api = 'https://api.coinone.co.kr/ticker?currency=allcoin'
        data = requests.get(api)
        return data.json()

    def post(self, request:Request):

        coin_data = config["coinone"]
        coin_list = coin_data.keys()
        od = OrderedDict(sorted(coin_data.items(), key=lambda x: x[1]['last'], reverse=True))

        print(od)
        # if coin_data is False:
        #     return NotFound
        #
        #
        # price = float(coin_data["last"])
        # currency = coin_data["currency"]
        # high = float(coin_data["high"])
        # low =float(coin_data["low"])
        # volume = float(coin_data["volume"])
        # serializer = serializers.CoinSerializer(price=price,currency=currency,high=high,low=low,volume=volume)

        return Response(status=status.HTTP_200_OK,data={"a":"a"})


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

        coin_data = config["upbit"]
        coin_list = []
        coin_serial = []
        print(coin_list)
        for j in coin_list:
            price = float(j[0]["trade_price"])
            currency = j[0]["market"].replace("KRW-","")
            high = float(j[0]["high_price"])
            low = float(j[0]["low_price"])
            volume = float(j[0]["acc_trade_volume"])
            model = models.Coin(price=price,currency=currency,high=high,low=low,volume=volume)
            coin_serial.append(model)
        serializer = serializers.CoinSerializer(coin_serial,many=True)

        return Response(status=status.HTTP_200_OK,data=serializer.data)

class Bithumb(APIView):

    def get_coin(self, name):
        api = f'https://api.bithumb.com/public/ticker/{name}'
        data = requests.get(api)
        if data.status_code == 400:
            return False
        return data.json()

    def post(self, request:Request):


        coin_data = config["bithumb"]

        if coin_data is False:
            return NotFound

        price = float(coin_data['data']["closing_price"])
        currency = name
        high = float(coin_data['data']["max_price"])
        low = float(coin_data['data']["min_price"])
        volume = float(coin_data['data']["units_traded_24H"])
        coin = models.Coin(price=price,name=currency,high=high,low=low,volume=volume)
        serializer = serializers.CoinSerializer(coin)

        return Response(status=status.HTTP_200_OK,data=serializer.data)


class KorBit(APIView):

    def get_coin(self, name):
        coin_name = f'{name.lower()}_krw'
        api = f'https://api.korbit.co.kr/v1/ticker/detailed?currency_pair={coin_name}'
        data = requests.get(api)
        if data.status_code == 400:
            return False
        return data.json()

    def post(self, request: Request):

        coin_data = config["korbit"]

        if coin_data is False:
            return NotFound

        price = float(coin_data["last"])
        currency = name
        high = float(coin_data["high"])
        low = float(coin_data["low"])
        volume = float(coin_data["volume"])

        serializer = serializers.CoinSerializer(price=price,currency=currency,high=high,low=low,volume=volume)

        return Response(status=status.HTTP_200_OK,data=serializer.data)


# Create your views here.
