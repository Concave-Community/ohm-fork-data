import csv
from datetime import datetime

import requests
import yaml

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
pools = fetch_curve_apy_volume()
today_date = datetime.today().strftime('%Y-%m-%d')
endpoint = 'https://speedy-nodes-nyc.moralis.io/6e55bded8312d1f70c28c678/eth/mainnet/archive'

data_dir = data_dir + '/curve_pools_' + today_date + '.csv'
with open(f"{data_dir}", "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(SNAPSHOT_COLUMNS)
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
