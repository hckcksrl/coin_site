import abc
from django.core.cache import cache

class CoinABCRepository:
    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def get_coin(self, site: str):
        pass



class CoinRepository(CoinABCRepository):
    def get_coin(self, site: str):
        coin_string_data = cache.get(site)
        coin_data_dict = json.loads(coin_string_data)
        coin_data = list(coin_data_dict.values())

        return coin_data