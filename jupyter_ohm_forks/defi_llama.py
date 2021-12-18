import pandas as pd
import requests


def add_defi_llama_data(df):
    session = requests.session()
    session.headers = {"Accept": "application/json"}

    uri = "https://api.llama.fi"

    data = session.get(f"{uri}/protocols").json()
    df_new = pd.DataFrame(data)
    df_new["symbol"] = df_new["symbol"].str.lower()
    df_new = df_new.add_prefix("dl_")

    return pd.merge(df, df_new, left_on="token_ticker", right_on="dl_symbol")
