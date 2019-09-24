from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
import json
import requests

NotFound = Response(status=status.HTTP_404_NOT_FOUND)

with open('/home/ubuntu/coin_chat/coin/exchange/config.json', 'r') as f:
    config = json.load(f)


def ko_or_en(name):
    k_count = 0
    for c in name:
        if ord('가') <= ord(c) <= ord('힣'):
            k_count += 1
            break
        elif ord('ㄱ') <= ord(c) <= ord('ㅎ'):
            k_count += 1
            break
    return False if k_count > 0 else True


def korean_to_english(name):
    if name in config:
        return config[name]
    else:
        return False

class CoinOne(APIView):

    def get_coin(self, name):
        api = f'https://api.coinone.co.kr/ticker?currency={name}'
        data = requests.get(api)
        if len(data.json()) != 14 or data.status_code == 404:
            return False
        return data.json()

    def post(self, request:Request):

        data = request.data
        name = data['action']['params']['coin']
        check = ko_or_en(name=name)
        if check is False:
            name = korean_to_english(name=name)

        if name is False:
            return NotFound

        coin_data = self.get_coin(name=name)

        if coin_data is False:
            return NotFound


        price = float(coin_data["last"])
        currency = coin_data["currency"]
        high = float(coin_data["high"])
        low =float(coin_data["low"])
        volumn = float(coin_data["volume"])

        return Response(status=status.HTTP_200_OK)


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

    def korean(self, name):
        api = f'https://api.upbit.com/v1/market/all'
        data = requests.get(api)
        check = data.json()

        for i in check:
            if name == i['korean_name']:
                s = i['market']
                if s.startswith('KRW'):
                    return s

        return False

    def post(self, request:Request):

        data = request.data
        name = data['action']['params']['coin']
        check = ko_or_en(name=name)

        if check is False:
            name = self.korean(name=name)

        if name is False:
            return NotFound

        coin_data = self.get_coin(name=name)

        if coin_data is False:
            return NotFound

        price = (coin_data[0]["trade_price"])
        currency = coin_data[0]["market"].replace("KRW-","")
        high = float(coin_data[0]["high_price"])
        low = float(coin_data[0]["low_price"])
        volumn = float(coin_data[0]["acc_trade_volume"])
        allprice = float(coin_data[0]["acc_trade_price"])


        return Response(status=status.HTTP_200_OK)


class Bithumb(APIView):

    def get_coin(self, name):
        api = f'https://api.bithumb.com/public/ticker/{name}'
        data = requests.get(api)
        if data.status_code == 400:
            return False
        return data.json()

    def post(self, request:Request):

        data = request.data
        name = data['action']['params']['coin']
        check = ko_or_en(name=name)
        if check is False:
            name = korean_to_english(name=name)

        if name is False:
            return NotFound

        coin_data = self.get_coin(name=name)

        if coin_data is False:
            return NotFound

        price = float(coin_data['data']["closing_price"])
        currency = name
        high = float(coin_data['data']["max_price"])
        low = float(coin_data['data']["min_price"])
        volumn = float(coin_data['data']["units_traded_24H"])
        allprice = float(coin_data['data']["acc_trade_value_24H"])
        fluctate = float(coin_data['data']["fluctate_rate_24H"])

        return Response(status=status.HTTP_200_OK)


class KorBit(APIView):

    def get_coin(self, name):
        coin_name = f'{name.lower()}_krw'
        api = f'https://api.korbit.co.kr/v1/ticker/detailed?currency_pair={coin_name}'
        data = requests.get(api)
        if data.status_code == 400:
            return False
        return data.json()

    def post(self, request: Request):

        data = request.data
        name = data['action']['params']['coin']
        check = ko_or_en(name=name)
        if check is False:
            name = korean_to_english(name=name)

        if name is False:
            return NotFound

        coin_data = self.get_coin(name=name)

        if coin_data is False:
            return NotFound

        price = float(coin_data["last"])
        currency = name
        high = float(coin_data["high"])
        low = float(coin_data["low"])
        volumn = float(coin_data["volume"])
        fluctate = float(coin_data["changePercent"])

        return Response(status=status.HTTP_200_OK)


# Create your views here.
