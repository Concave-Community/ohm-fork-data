class CurveCoin(object):
    address: str
    usdPrice: float
    decimals: int
    symbol: str
    poolBalance: int

    def __init__(self, coin_dict: dict):
        self.address = coin_dict['address']
        self.usdPrice = coin_dict['usdPrice']
        if int(coin_dict["decimals"]) == 0:
            self.decimals = 1
        else:
            self.decimals = int(coin_dict['decimals'])
        self.symbol = coin_dict['symbol']
        self.poolBalance = int(coin_dict['poolBalance'])
