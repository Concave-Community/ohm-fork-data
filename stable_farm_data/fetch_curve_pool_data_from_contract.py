import json

import web3

abi_dir = "../abis/stable_farms/curve"


def fetch_balance_from_contract(pool_name, endpoint):
    try:
        w3 = web3.Web3(web3.Web3.HTTPProvider(endpoint))
        pool_data_json = json.loads(open(f"{abi_dir}/{pool_name}/pooldata.json").read())
        token_contract = w3.eth.contract(
            web3.Web3.toChecksumAddress(pool_data_json['swap_address']),
            abi=open(f"{abi_dir}/{pool_name}/abi.json").read(),
        )

        total_balance = {}
        for i in range(len(pool_data_json['coins'])):
            coin = pool_data_json['coins'][i]
            print(coin)
            balance_of_coin = token_contract.caller.balances(i)
            decimal = coin['decimals']
            total_balance[coin['name']] = balance_of_coin / (pow(10, decimal))
        return total_balance
    except Exception:
        return {}

