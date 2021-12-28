import requests
import pandas as pd
import numpy as np
import os.path as ospath
import time


def get_closest(prices_df, timestamp):
    i = np.argmin(np.abs(prices_df.timestamp - timestamp))

    return float(prices_df.iloc[i].price)


def get_price_by_ts(fork_name, symbol, timestamp):

    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart/range"
    params = {"vs_currency": "usd", "from": time.time(), "to": time.time()}

    if ospath.exists(f"./data/{fork_name}/{symbol}.csv"):
        prices_df = pd.read_csv(f"./data/{fork_name}/{symbol}.csv")

        params["from"] = float(prices_df.sort_values(by="timestamp").tail(1).timestamp)

    else:
        params["from"] = timestamp
        prices_df = None

    if params["from"] <= timestamp:
        new_prices = requests.get(url, params=params).json().get("prices")
        new_prices = [[int(data[0] / 1000), data[1]] for data in new_prices]
        new_prices_df = pd.DataFrame(new_prices, columns=["timestamp", "price"])

        if prices_df:
            prices_df = prices_df + new_prices_df
        else:
            prices_df = new_prices_df

    prices_df.to_csv(f"./data/{fork_name}/{symbol}.csv", index=False)

    return get_closest(prices_df, timestamp)
