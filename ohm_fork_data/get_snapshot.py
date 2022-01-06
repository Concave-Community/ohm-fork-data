import web3
import yaml
import csv
import math
import requests

SNAPSHOT_COLUMNS = [
    "name",
    "total_supply",
    "staked_supply",
    "market_price",
    "five_day_rate",
    "staking_apy",
    "index",
    "staking_tvl",
    "market_cap",
    "staking_ratio",
]

wonderland_clones = [
    "wonderland",
    "umami-finance",
    "fortressdao",
    "life-dao",
    "snowbank",
    "maximizer",
    "o2-dao",
    "piggy-bank",
    "r-u-generous",
    "galaxygoggle"
]

DEFAULT_REBASE_INTERVAL = 8
special_rebase_interval = {
    "metaversepro": 1
}


def save_snapshot_data(writer, fork, chain, endpoint, abi_dir, data_dir, moralis_key):
    w3 = web3.Web3(web3.Web3.HTTPProvider(endpoint))

    if chain == "avalanche":
        w3.middleware_onion.inject(web3.middleware.geth_poa_middleware, layer=0)

    token_contract = w3.eth.contract(
        web3.Web3.toChecksumAddress(fork.get("token_address")),
        abi=open(f"{abi_dir}/{fork.get('token_abi')}").read(),
    )
    staked_contract = w3.eth.contract(
        web3.Web3.toChecksumAddress(fork.get("staked_address")),
        abi=open(f"{abi_dir}/{fork.get('staked_abi')}").read(),
    )
    staking_contract = w3.eth.contract(
        web3.Web3.toChecksumAddress(fork.get("staking_address")),
        abi=open(f"{abi_dir}/{fork.get('staking_abi')}").read(),
    )

    epoch = staking_contract.functions.epoch().call()

    # time modified epoch code, this fixes it
    if fork.get("name") in wonderland_clones:
        epoch = [epoch[2], epoch[0], epoch[3], epoch[1]]

    staking_reward = epoch[3] / math.pow(10, 9)
    staked_supply = staked_contract.functions.circulatingSupply().call() / math.pow(
        10, 9
    )
    staking_rebase = staking_reward / staked_supply

    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={fork.get('name')}&vs_currencies=usd"
        json = requests.get(url).json()
        market_price = json[fork.get("name")]["usd"]
    except KeyError:
        market_price = 0.0

    total_supply = token_contract.functions.totalSupply().call() / math.pow(10, 9)

    rebase_interval = special_rebase_interval.get(fork.get('name'), DEFAULT_REBASE_INTERVAL)
    rebase_time_per_day = 24 / rebase_interval

    writer.writerow(
        [
            fork.get("name"),
            total_supply,
            staked_supply,
            market_price,
            100 * (math.pow(1 + staking_rebase, 5 * rebase_time_per_day) - 1),
            100 * (math.pow(1 + staking_rebase, 365 * rebase_time_per_day) - 1),
            staking_contract.functions.index().call() / math.pow(10, 9),
            staked_supply * market_price,
            total_supply * market_price,
            staked_supply / total_supply,
        ]
    )


with open("forks-snapshot.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)

abi_dir = config.get("abi_dir", "./abi")
data_dir = config.get("data_dir", "./data")
moralis_key = config.get("moralis_key")

with open(f"{data_dir}/snapshot.csv", "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(SNAPSHOT_COLUMNS)

    for chain in config.get("chains"):
        print("dealing with chain:" + str(chain))
        chain_name = chain.get("name")
        endpoint = chain.get("endpoint")

        w3 = web3.Web3(web3.Web3.HTTPProvider(endpoint))

        for fork in chain.get("forks", None):
            fork_name = fork.get("name")

            print("saving snapshot for fork=" + fork_name)

            save_snapshot_data(
                writer, fork, chain_name, endpoint, abi_dir, data_dir, moralis_key
            )
