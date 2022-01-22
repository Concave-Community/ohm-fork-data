import csv

import requests
import yaml

from stable_farm_data.CurvePool import CurvePool
from stable_farm_data.fetch_data_from_contract import fetch_balance_from_contract

pool_names = ["compound", "usdt", "y", "busd", "susd", "pax", "ren2", "rens", "hbtc", "3pool", "gusd", "husd", "usdn",
              "usdk", "linkusd", "musd", "rsv", "tbtc", "dusd", "pbtc", "bbtc", "obtc", "ust", "eurs", "seth", "aave",
              "idle", "steth", "saave", "ankreth", "ib", "link", "usdp", "tusd", "frax", "lusd", "busdv2", "alusd",
              "reth", "mim", "eurt", "rai"]

SNAPSHOT_COLUMNS = [
    "date",
    "name",
    "daily_apy",
    "weekly_apy",
    "monthly_apy",
    "total_apy",
    "volume",
    "tvl",
]

data_dir = "../data/stable_farms"

CURVE_APY_VOLUMN_URL = "https://stats.curve.fi/raw-stats/apys.json"
# CURVE_FACTORY_V2_POOL = "https://api.curve.fi/api/getFactoryV2Pools"
# CURVE_FACTORY_APy = "https://api.curve.fi/api/getFactoryAPYs?version=2"
CURVE_POOL_TVL = "https://api.curve.fi/api/getTVLCrypto"

apy_volumn = requests.get(CURVE_APY_VOLUMN_URL).json()
# factory_v2_pool = requests.get(CURVE_FACTORY_V2_POOL).json()
# factory_apy = requests.get(CURVE_FACTORY_APy).json()
pool_tvl = requests.get(CURVE_POOL_TVL).json()

daily_apy_dict = apy_volumn['apy']['day']
weekly_apy_dict = apy_volumn['apy']['week']
monthly_apy_dict = apy_volumn['apy']['month']
total_apy_dict = apy_volumn['apy']['total']
volume_dict = apy_volumn['volume']

pools = []

for key in daily_apy_dict:
    daily_apy = daily_apy_dict[key]
    weekly_apy = weekly_apy_dict[key]
    monthly_apy = monthly_apy_dict[key]
    total_apy = total_apy_dict[key]
    volume = volume_dict.get(key, 0)
    curve_pool = CurvePool(name=key, daily_apy=daily_apy, weekly_apy=weekly_apy,
                           monthly_apy=monthly_apy, total_apy=total_apy, volume=volume)
    pools.append(curve_pool)

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
        for farm in farms:
            if farm.get('name') == pool.pool_name:
                tvl = fetch_balance_from_contract(farm.get('pool_address'), endpoint)

        writer.writerow(
            [
                pool.snapshot_timestamp,
                pool.pool_name,
                pool.daily_apy,
                pool.weekly_apy,
                pool.monthly_apy,
                pool.total_apy,
                pool.volume,
                tvl
            ]
        )
