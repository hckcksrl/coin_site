from ..repository import *


class CoinInteractor:
    def __init__(self):
        self.repository = CoinRepository()


class GetCoinInteractor(CoinInteractor):
    def execute(self, site: str):
        return self.repository.get_coin(site=site)

