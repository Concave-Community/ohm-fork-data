import csv

import requests
import yaml

from stable_farm_data.Pool import Pool
from stable_farm_data.farm_api_adapter import fetch_curve_apy_volume
from stable_farm_data.fetch_curve_pool_data_from_contract import fetch_balance_from_contract
from utils.collection_utils import get_with_default
from utils.token_sympol_mapping import fetch_real_price_in_usd

pool_names = ["compound", "usdt", "y", "busd", "susd", "pax", "ren2", "rens", "hbtc", "3pool", "gusd", "husd", "usdn",
              "usdk", "linkusd", "musd", "rsv", "tbtc", "dusd", "pbtc", "bbtc", "obtc", "ust", "eurs", "seth", "aave",
              "idle", "steth", "saave", "ankreth", "ib", "link", "usdp", "tusd", "frax", "lusd", "busdv2", "alusd",
              "reth", "mim", "eurt", "rai"]

SNAPSHOT_COLUMNS = [
    "date",
    "pool_name",
    "daily_apy",
    "weekly_apy",
    "monthly_apy",
    "total_apy",
    "volume_in_usd",
    "token1",
    "token1_tvl_in_usd",
    "token2",
    "token2_tvl_in_usd",
    "token3",
    "token3_tvl_in_usd",
    "token4",
    "token4_tvl_in_usd",
    "total_tvl_in_usd",
]

data_dir = "../data/stable_farms"

# CURVE_FACTORY_V2_POOL = "https://api.curve.fi/api/getFactoryV2Pools"
# CURVE_FACTORY_APY = "https://api.curve.fi/api/getFactoryAPYs?version=2"
CURVE_POOL_TVL = "https://api.curve.fi/api/getTVLCrypto"

# factory_v2_pool = requests.get(CURVE_FACTORY_V2_POOL).json()
# factory_apy = requests.get(CURVE_FACTORY_APy).json()
pool_tvl = requests.get(CURVE_POOL_TVL).json()


pools = fetch_curve_apy_volume()

with open("../stable-farms.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)
data_dir = data_dir + '/curve_pools.csv'
with open(f"{data_dir}", "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(SNAPSHOT_COLUMNS)
    endpoint = config.get('endpoint')
    farms = config.get('farms')
    for pool in pools:
        tvl = 0
        tvl_dict = fetch_balance_from_contract(pool_name=pool.pool_name,
                                               endpoint=endpoint)
        if len(tvl_dict) == 0:
            continue
        token_names = list(tvl_dict.keys())
        real_price_map = fetch_real_price_in_usd(token_names)
        token1_name = get_with_default(token_names, 0, "")
        token1_tvl = tvl_dict.get(token1_name, 0) * real_price_map.get(token1_name, 1)
        token2_name = get_with_default(token_names, 1, "")
        token2_tvl = tvl_dict.get(token2_name, 0) * real_price_map.get(token2_name, 1)
        token3_name = get_with_default(token_names, 2, "")
        token3_tvl = tvl_dict.get(token3_name, 0) * real_price_map.get(token3_name, 1)
        token4_name = get_with_default(token_names, 3, "")
        token4_tvl = tvl_dict.get(token4_name, 0) * real_price_map.get(token4_name, 1)
        total_tvl = token1_tvl + token2_tvl + token3_tvl + token4_tvl
        writer.writerow(
            [
                pool.snapshot_timestamp,
                pool.pool_name,
                pool.daily_apy,
                pool.weekly_apy,
                pool.monthly_apy,
                pool.total_apy,
                pool.volume,
                token1_name,
                token1_tvl,
                token2_name,
                token2_tvl,
                token3_name,
                token3_tvl,
                token4_name,
                token4_tvl,
                total_tvl
            ]
        )
