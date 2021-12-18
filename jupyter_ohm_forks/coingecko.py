import requests
import pandas as pd


def add_coingecko_data(df):
    session = requests.session()
    session.headers = {"Accept": "application/json"}

    uri = "https://api.coingecko.com"
    coins = "%2C".join(df["name"])
    path = f"api/v3/coins/markets?vs_currency=usd&ids={coins}"

    data = session.get(f"{uri}/{path}").json()
    df_new = pd.DataFrame(data)
    df_new = df_new.add_prefix("cg_")

    return pd.merge(df, df_new, left_on="token_ticker", right_on="cg_symbol")
