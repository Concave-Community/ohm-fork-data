import math
import requests
from web3 import Web3
import pandas as pd

def get_price(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    return requests.get(url).json()[symbol]['usd']

def add_on_chain_data(df):

    on_chain_data = []

    for idx, row in df.iterrows():
        w3 = Web3(Web3.HTTPProvider(row['api']))

        token_abi = open(f"abis/{row['token_abi']}", "r").read()
        staked_abi = open(f"abis/{row['staked_abi']}", "r").read()
        staking_abi = open(f"abis/{row['staking_abi']}", "r").read()
        supply_abi = open(f"abis/{row['supply_abi']}", "r").read()

        token_contract = w3.eth.contract(Web3.toChecksumAddress(row['token_contract']), abi=token_abi)
        staked_contract = w3.eth.contract(Web3.toChecksumAddress(row['staked_contract']), abi=staked_abi)
        staking_contract = w3.eth.contract(Web3.toChecksumAddress(row['staking_contract']), abi=staking_abi)
        supply_contract = w3.eth.contract(Web3.toChecksumAddress(row['supply_contract']), abi=supply_abi)

        data = {}
        data['oc_token_ticker'] = row['token_ticker']

        data['oc_total_supply'] = token_contract.functions.totalSupply().call() / math.pow(10, 9)
        staked_circ_supply = staked_contract.functions.circulatingSupply().call() / math.pow(10, 9)

        data["oc_current_block"] = w3.eth.block_number

        data['oc_market_price'] = get_price(row['name'])
        circ_supply_function = getattr(supply_contract.functions, f"{row['token_ticker'].upper()}CirculatingSupply")
        circ_supply = circ_supply_function().call() / math.pow(10, 9)

        data['oc_epoch'] = staking_contract.functions.epoch().call()
        staking_reward = data['oc_epoch'][3] / math.pow(10, 9)
        data["oc_staking_rebase"] = staking_reward / staked_circ_supply
        data["oc_five_day_rate"] = math.pow(1 + data["oc_staking_rebase"], 5 * 3) - 1
        data["oc_staking_apy"] = math.pow(1 + data["oc_staking_rebase"], 365 * 3) - 1
        data["oc_index"] = staking_contract.functions.index().call() / math.pow(10, 9)
        data["oc_next_rebase"] = data['oc_epoch'][2]
        data["oc_staking_tvl"] = staked_circ_supply * data["oc_market_price"]
        data["oc_market_cap"] = circ_supply * data["oc_market_price"]
        data["oc_staking_ratio"] = staked_circ_supply / circ_supply

        on_chain_data.append(data)

    df_new = pd.DataFrame(on_chain_data)
    return pd.merge(df, df_new, left_on="token_ticker", right_on="oc_token_ticker")