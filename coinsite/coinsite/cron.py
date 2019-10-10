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
            korean = data[name]
            currency = name
            high = coin["high"]
            low = coin["low"]
            volume = round(coin["volume"], 2)
            coin_data.update({name: {
                "currency": currency,
                "price": price,
                "high": high,
                "low": low,
                "volume": volume,
                "korean": korean
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
            korean = data[name]
            currency = name
            high = float(coin[0]["high_price"])
            low = float(coin[0]["low_price"])
            volume = round(float(coin[0]["acc_trade_volume"]), 2)
            coin_data.update({name: {
                "currency": currency,
                "price": price,
                "high": high,
                "low": low,
                "volume": volume,
                "korean": korean
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
            korean = data[name]
            currency = name
            high = float(coin['data']["max_price"])
            low = float(coin['data']["min_price"])
            volume = round(float(coin['data']["units_traded_24H"]), 2)
            coin_data.update({name: {
                "currency": currency,
                "price": price,
                "high": high,
                "low": low,
                "volume": volume,
                "korean": korean
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
            korean = data[name]
            currency = name
            high = float(coin["high"])
            low = float(coin["low"])
            volume = round(float(coin["volume"]), 2)
            coin_data.update({name: {
                "currency": currency,
                "price": price,
                "high": high,
                "low": low,
                "volume": volume,
                "korean": korean
            }})

        return json.dumps(coin_data)


def set_redis():
# if __name__ == '__main__':

    coinone_coin = CoinOne().get_coinone()
    upbit_coin = Upbit().get_upbit()
    bithumb_coin = Bithumb().get_bithumb()
    korbit_coin = Korbit().get_korbit()


    cache.delete('coinone')
    cache.set('coinone', coinone_coin)

    cache.delete('upbit')
    cache.set('upbit', upbit_coin)

    cache.delete('bithumb')
    cache.set('bithumb', bithumb_coin)

    cache.delete('korbit')
    cache.set('korbit',korbit_coin)

# else :
#
#     print(False)
