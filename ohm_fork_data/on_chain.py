import web3
import math
import pandas as pd
import os.path as ospath

from ohm_fork_data.moralis import MoralisPy

FORK_COLUMNS = (
    "fork",
    "block",
    "timestamp",
    "supply",
    "staked",
    "index",
    "market_price",
    "length",
    "number",
    "end_block",
    "distribute",
)
BOND_COLUMNS = (
    "name",
    "block",
    "timestamp",
    "price",
    "add",
    "rate",
    "target",
    "buffer",
    "last_time",
    "control_variable",
    "min_price",
    "max_payout",
    "max_debt",
    "vesting_term",
)
TREASURY_COLUMNS = ("name", "block", "timestamp", "quantity", "value")


def save_block_data(fork, chain, block, endpoint, abi_dir, data_dir, moralis_key):
    w3 = web3.Web3(web3.Web3.HTTPProvider(endpoint))
    moralis = MoralisPy()
    moralis.set_api_key(moralis_key)

    # avax requires special middleware
    if chain == "avalanche":
        w3.middleware_onion.inject(web3.middleware.geth_poa_middleware, layer=0)

    timestamp = w3.eth.get_block(block).timestamp
    market_price = moralis.get_token_price(fork.get("token_address"), chain, block).get(
        "usdPrice"
    )

    save_staking_data(
        w3, fork, chain, block, timestamp, market_price, data_dir, abi_dir
    )
    save_bond_data(w3, fork, block, timestamp, data_dir, abi_dir)
    save_treasury_data(w3, fork, block, timestamp, data_dir, moralis)


def save_staking_data(
    w3, fork, chain, block, timestamp, market_price, data_dir, abi_dir
):

    # Staking Collection
    if ospath.exists(f"{data_dir}/{fork.get('name')}/{fork.get('name')}_fork.csv"):
        fork_data_df = pd.read_csv(
            f"{data_dir}/{fork.get('name')}/{fork.get('name')}_fork.csv"
        )
    else:
        fork_data_df = pd.DataFrame([], columns=FORK_COLUMNS)

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

    epoch = staking_contract.functions.epoch().call(block_identifier=block)

    # time modified epoch code, this fixes it
    if fork.get("name") == "wonderland":
        epoch = [epoch[2], epoch[0], epoch[3], epoch[1]]

    fork_row_df = pd.DataFrame(
        [
            [
                fork.get("name"),
                block,
                timestamp,
                token_contract.functions.totalSupply().call(block_identifier=block)
                / math.pow(10, 9),
                staked_contract.functions.circulatingSupply().call(
                    block_identifier=block
                )
                / math.pow(10, 9),
                (staking_contract.functions.index().call(block_identifier=block)
                / math.pow(10, 9)) / fork.get('initial_index', 1),
                market_price,
            ]
            + epoch[:-1]
            + [epoch[3] / math.pow(10, 9)]
        ],
        columns=FORK_COLUMNS,
    )

    fork_data_df = fork_data_df.append(fork_row_df)
    fork_data_df.to_csv(
        f"{data_dir}/{fork.get('name')}/{fork.get('name')}_fork.csv", index=False
    )

    return True


def save_treasury_data(w3, fork, block, timestamp, data_dir, moralis):

    if ospath.exists(f"{data_dir}/{fork.get('name')}/{fork.get('name')}_treasury.csv"):
        treasury_data_df = pd.read_csv(
            f"{data_dir}/{fork.get('name')}/{fork.get('name')}_treasury.csv"
        )
    else:
        treasury_data_df = pd.DataFrame([], columns=TREASURY_COLUMNS)

    treasury = {}

    for asset in fork.get("treasury_addresses"):
        treasury_row = moralis.get_total_token_assets(
            asset.get("address"), [asset.get("chain")]
        )

        for row in treasury_row:
            if treasury.get(row["symbol"], None):
                treasury[row["symbol"]]["quantity"] += row["quantity"]
                treasury[row["symbol"]]["value"] += row["holdings_value_usd"]
            else:
                treasury[row["symbol"]] = {
                    "quantity": row["quantity"],
                    "value": row["holdings_value_usd"],
                }

    treasury_rows = [
        [k, block, timestamp, v["quantity"], v["value"]] for k, v in treasury.items()
    ]

    treasury_data_df = treasury_data_df.append(
        pd.DataFrame(treasury_rows, columns=TREASURY_COLUMNS)
    )
    treasury_data_df.to_csv(
        f"{data_dir}/{fork.get('name')}/{fork.get('name')}_treasury.csv", index=False
    )

    return True


def save_bond_data(w3, fork, block, timestamp, data_dir, abi_dir):

    if ospath.exists(f"{data_dir}/{fork.get('name')}/{fork.get('name')}_bonds.csv"):
        bond_data_df = pd.read_csv(
            f"{data_dir}/{fork.get('name')}/{fork.get('name')}_bonds.csv"
        )
    else:
        bond_data_df = pd.DataFrame([], columns=BOND_COLUMNS)

    bond_rows = []

    for bond in fork.get("bonds"):
        bond_contract = w3.eth.contract(
            web3.Web3.toChecksumAddress(bond.get("address")),
            abi=open(f"{abi_dir}/{fork.get('bond_abi')}").read(),
        )

        try:
            terms = bond_contract.functions.terms().call(block_identifier=block)

            if fork == "time":
                terms = [terms[0], terms[4], terms[1], terms[2], terms[3]]

            bond_rows.append(
                [
                    bond.get("name"),
                    block,
                    timestamp,
                    bond_contract.functions.bondPrice().call(block_identifier=block),
                ]
                + bond_contract.functions.adjustment().call(block_identifier=block)
                + terms
            )
        except:
            continue

        bond_data_df = bond_data_df.append(
            pd.DataFrame(bond_rows, columns=BOND_COLUMNS)
        )
        bond_data_df.to_csv(
            f"{data_dir}/{fork.get('name')}/{fork.get('name')}_bonds.csv", index=False
        )

    return True
