from json import JSONEncoder

from models.curve_coin import CurveCoin


class CurveFactoryMetaPool(object):
    id: str
    address: str
    coinsAddresses: [str]
    decimals: [int]
    underlyingDecimals: [int]
    assetType: str
    name: str
    symbol: str
    totalSupply: int
    implementation: str
    coins: [CurveCoin]
    usdTotal: float

    def __init__(self, pool_dict: dict, pool_apy_dict: dict):
        self.id = pool_dict['id']
        self.address = pool_dict['address']
        self.coinsAddresses = pool_dict['coinsAddresses']
        self.decimals = pool_dict['decimals']
        self.underlyingDecimals = pool_dict['underlyingDecimals']
        self.assetType = pool_dict['assetType']
        self.name = pool_dict['name']
        self.totalSupply = pool_dict['totalSupply']
        self.implementation = pool_dict['implementation']
        self.usdTotal = pool_dict['usdTotal']
        self.apy = pool_apy_dict['apy']
        self.volume = pool_apy_dict['volume']
        coins: [CurveCoin] = pool_dict['coins']
        self.coins = []
        for coin_dict in coins:
            coin = CurveCoin(coin_dict)
            self.coins.append(coin)
