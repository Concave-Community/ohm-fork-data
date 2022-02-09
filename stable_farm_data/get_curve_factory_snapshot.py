import csv
from datetime import datetime

import yaml

from stable_farm_data.farm_api_adapter import fetch_curve_factory_pool

pool_names = ["UST_whv23CRV-f"]

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

pools = fetch_curve_factory_pool()
today_date = datetime.today().strftime('%Y-%m-%d')

with open("../stable-farms.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)
data_dir = data_dir + '/curve_factory_pools_' + today_date + '.csv'
with open(f"{data_dir}", "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(SNAPSHOT_COLUMNS)
    endpoint = config.get('endpoint')
    farms = config.get('farms')
    for pool in pools:
        coins = pool.coins
        token1_name = ""
        token1_tvl = 0
        token2_name = ""
        token2_tvl = 0
        token3_name = ""
        token3_tvl = 0
        token4_name = ""
        token4_tvl = 0
        if len(coins) >= 1:
            token1_name = coins[0].symbol
            token1_tvl = coins[0].poolBalance / pow(10, coins[0].decimals) * coins[0].usdPrice
        if len(coins) >= 2:
            token2_name = coins[1].symbol
            token2_tvl = coins[1].poolBalance / pow(10, coins[1].decimals) * coins[1].usdPrice
        if len(coins) >= 3:
            token3_name = coins[2].symbol
            token3_tvl = coins[2].poolBalance / pow(10, coins[2].decimals) * coins[2].usdPrice
        if len(coins) >= 4:
            token4_name = coins[3].symbol
            token4_tvl = coins[3].poolBalance / pow(10, coins[3].decimals) * coins[3].usdPrice
        total_tvl = token1_tvl + token2_tvl + token3_tvl + token4_tvl
        writer.writerow(
            [
                today_date,
                pool.name,
                pool.apy,
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
