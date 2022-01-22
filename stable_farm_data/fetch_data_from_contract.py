import json

import web3

abi_dir = "../abis/stable_farms/curve/3pool"


def fetch_balance_from_contract(contract_address, endpoint):
    w3 = web3.Web3(web3.Web3.HTTPProvider(endpoint))
    token_contract = w3.eth.contract(
        web3.Web3.toChecksumAddress(contract_address),
        abi=open(f"{abi_dir}/abi.json").read(),
    )

    pool_data_json = json.loads(open(f"{abi_dir}/pooldata.json").read())
    total_balance = 0
    for i in range(len(pool_data_json['coins'])):
        print(pool_data_json['coins'][i])
        balance_of_coin = token_contract.caller.balances(i)
        decimal = pool_data_json['coins'][i]['decimals']
        total_balance += balance_of_coin / (pow(10, decimal))
    return total_balance
