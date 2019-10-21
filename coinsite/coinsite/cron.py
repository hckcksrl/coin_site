import requests
import json
import time
from django.core.cache import cache
import os
import sys
with open(os.path.join(sys.path[0], "coinsite/config.json"), 'r') as f:
    config = json.load(f)


class CoinOne():

    def __init__(self):
        pass

    def get_coin(self, name):
        api = f'https://api.coinone.co.kr/ticker?currency=BTC'
        data = requests.get(api)
        return data.json()

    def get_coinone(self):
        data = config["coinone"]
        coin_list = list(data.keys())
        coin_data = dict()
        for name in coin_list:
            coin = self.get_coin(name=name)
            price = float(coin["last"])
            korean = data[name]
            currency = name
            high = coin["high"]
            low = coin["low"]
            volume = round(float(coin["volume"]), 2)

            yesterday = float(coin["yesterday_last"])   # 24시간전 마지막가격
            rate = round(((price/yesterday)-1)*100,2) # 24시간전가격, 지금가격의 가격등락폭

            coin_data.update({name: {
                "currency": currency,
                "price": price,
                "high": high,
                "low": low,
                "volume": volume,
                "korean": korean,
                "rate" : rate
            }})

        return json.dumps(coin_data)


class Upbit:

    def __init__(self):
        pass

    def get_coin(self, name):
        name = name.upper()
        second_count = 0
        if not name.startswith('KRW-'):
            name = f'KRW-{name}'
        api = f'https://api.upbit.com/v1/ticker?markets={name}'
        data = requests.get(api)

        remain_req = data.headers['Remaining-Req']
        remain_str = remain_req.split(';')
        for i in range(2, 3):
            second_count= remain_str[i].split('=')[1]

        if int(second_count) == 1:
            time.sleep(1)

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
            rate = round(float(coin[0]["change_rate"])*100, 2)
            change = coin[0]["change"]
            if change == 'FALL':
                rate = 0 - rate
            coin_data.update({name: {
                "currency": currency,
                "price": price,
                "high": high,
                "low": low,
                "volume": volume,
                "korean": korean,
                "rate": rate
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
            rate = float(coin['data']["fluctate_rate_24H"])
            coin_data.update({name: {
                "currency": currency,
                "price": price,
                "high": high,
                "low": low,
                "volume": volume,
                "korean": korean,
                "rate": rate
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
            rate = float(coin["changePercent"])
            coin_data.update({name: {
                "currency": currency,
                "price": price,
                "high": high,
                "low": low,
                "volume": volume,
                "korean": korean,
                "rate": rate
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
