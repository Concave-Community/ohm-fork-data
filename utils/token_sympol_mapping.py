import requests

from utils.collection_utils import get_dict_key_by_value

coingeck_token_code_mapping = {
    "3CRV": "lp-3pool-curve",
    "DAI": "dai",
    "GUSD": "gemini-dollar",
    "DUSD": "defidollar",
    "bBTC": "binance-wrapped-btc",
    "UST": "terrausd",
    "aDAI": "aave-dai",
    "aUSDC": "aave-usdc",
    "USDC": "usd-coin",
    "USDT": "tether",
}


def fetch_real_price_in_usd(token_list):
    try:
        mapping_tokens = []
        for token in token_list:
            mapping_token = coingeck_token_code_mapping.get(token)
            if mapping_token is not None:
                mapping_tokens.append(mapping_token)
        token_param = ",".join(mapping_tokens)
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_param}&vs_currencies=usd"
        fetched_result = requests.get(url).json()
        # market_price = json[fork.get("name")]["usd"]
        real_market_price = {}
        for key, value in fetched_result.items():
            real_market_price[get_dict_key_by_value(coingeck_token_code_mapping, key)] = value['usd']
        return real_market_price
    except KeyError:
        pass


if __name__ == '__main__':
    token_list = list(coingeck_token_code_mapping.keys())
    print("token_list_length:" + str(len(token_list)))
    print(token_list)
    price_list = fetch_real_price_in_usd(token_list)
    print("price_list_length:" + str(len(price_list)))
    print(price_list)
