from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
from django.core.cache import cache
import json
from . import serializers
from .interactors import GetCoinInteractor

class GetCoin(APIView):

    def get(self, request: Request, site):

        coins = GetCoinInteractor().execute(site=site)
        serializer = serializers.CoinSerializer(coins, many=True)

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

