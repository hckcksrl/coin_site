import requests
import redis
import json
from django.core.cache import cache


with open('/Users/hckcksrl/Desktop/study/coinsite/coinsite/coinsite/config.json', 'r') as f:
    config = json.load(f)


class CoinOne():

    def __init__(self):
        pass

    def get_coin(self, name):
        api = f'https://api.coinone.co.kr/ticker?currency={name}'
        data = requests.get(api)
        return data.json()

    def get_coinone(self):
        data = config["coinone"]
        coin_list = list(data.keys())
        coin_data = dict()
        for name in coin_list:
            coin = self.get_coin(name=name)
            price = coin["last"]
            currency = coin["currency"].upper()
            high = coin["high"]
            low = coin["low"]
            volume = coin["volume"]
            coin_data.update({name: {
                "currency": currency,
                "price": price,
                "high": high,
                "low": low,
                "volume": volume,
            }})

        return json.dumps(coin_data)


class Upbit:

    def __init__(self):
        pass

    def get_coin(self, name):
        name = name.upper()
        if not name.startswith('KRW-'):
            name = f'KRW-{name}'
        api = f'https://api.upbit.com/v1/ticker?markets={name}'
        data = requests.get(api)

        if data.status_code == 404:
            return False
        return data.json()

    def get_upbit(self):

        data = config["upbit"]
        coin_list = list(data.keys())
        coin_data = dict()
        for name in coin_list:
            coin = self.get_coin(name=name)
            price = float(coin[0]["trade_price"])
            currency = name
            high = float(coin[0]["high_price"])
            low = float(coin[0]["low_price"])
            volume = float(coin[0]["acc_trade_volume"])
            coin_data.update({name: {
                "currency": currency,
                "price": price,
                "high": high,
                "low": low,
                "volume": volume,
            }})

        return json.dumps(coin_data)


class Bithumb:

    def __init__(self):
        pass

    def get_coin(self, name):
        api = f'https://api.bithumb.com/public/ticker/{name}'
        data = requests.get(api)
        if data.status_code == 400:
            return False
        return data.json()

    def get_bithumb(self):

        data = config["bithumb"]
        coin_list = list(data.keys())
        coin_data = dict()
        for name in coin_list:
            coin = self.get_coin(name=name)
            price = float(coin['data']["closing_price"])
            currency = name
            high = float(coin['data']["max_price"])
            low = float(coin['data']["min_price"])
            volume = float(coin['data']["units_traded_24H"])
            coin_data.update({name: {
                "currency": currency,
                "price": price,
                "high": high,
                "low": low,
                "volume": volume,
            }})

        return json.dumps(coin_data)


class Korbit:

    def __init__(self):
        pass

    def get_coin(self, name):
        coin_name = f'{name.lower()}_krw'
        api = f'https://api.korbit.co.kr/v1/ticker/detailed?currency_pair={coin_name}'
        data = requests.get(api)
        if data.status_code == 400:
            return False
        return data.json()

    def get_korbit(self):

        data = config["korbit"]
        coin_list = list(data.keys())
        coin_data = dict()
        for name in coin_list:
            coin = self.get_coin(name=name)
            price = float(coin["last"])
            currency = name
            high = float(coin["high"])
            low = float(coin["low"])
            volume = float(coin["volume"])
            coin_data.update({name: {
                "currency": currency,
                "price": price,
                "high": high,
                "low": low,
                "volume": volume,
            }})

        return json.dumps(coin_data)


def set_redis():
# if __name__ == '__main__':

    cache.delete('coinone')
    cache.delete('upbit')
    cache.delete('bithumb')
    cache.delete('korbit')

    coinone_coin = CoinOne().get_coinone()
    upbit_coin = Upbit().get_upbit()
    bithumb_coin = Bithumb().get_bithumb()
    korbit_coin = Korbit().get_korbit()

    cache.set('coinone',coinone_coin)
    cache.set('upbit',upbit_coin)
    cache.set('bithumb',bithumb_coin)
    cache.set('korbit',korbit_coin)

# else :
#
#     print(False)
