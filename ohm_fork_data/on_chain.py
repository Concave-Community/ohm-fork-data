import web3
import requests
from web3 import contract
import yaml
import csv
import math

from ohm_fork_data.get_price import get_price_by_ts


def save_block_data(fork, chain, block, endpoint, abi_dir, data_dir):
    w3 = web3.Web3(web3.Web3.HTTPProvider(endpoint))

    # avax requires special middleware
    if chain == "avax":
        w3.middleware_onion.inject(web3.middleware.geth_poa_middleware, layer=0)

    timestamp = w3.eth.get_block(block).timestamp
    market_price = get_price_by_ts(fork.get("name"), fork.get("name"), timestamp)

    with open(f"{data_dir}/{fork.get('name')}/{fork.get('name')}_fork.csv", "a+") as f:
        fork_data = csv.writer(f)

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
        if fork.get("name") == "time":
            epoch = [epoch[2], epoch[0], epoch[3], epoch[1]]

        fork_row = (
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
                staking_contract.functions.index().call(block_identifier=block)
                / math.pow(10, 9),
                market_price,
            ]
            + epoch[:-1]
            + [epoch[3] / math.pow(10, 9)]
        )

        fork_data.writerow(fork_row)

    with open(
        f"{data_dir}/{fork.get('name')}/{fork.get('name')}_treasury.csv", "a+"
    ) as f:
        treasury_data = csv.writer(f)
        treasury_rows = []

        for asset in fork.get("treasury"):
            asset_contract = w3.eth.contract(
                web3.Web3.toChecksumAddress(asset.get("address")),
                abi=open(f"{abi_dir}/{asset.get('abi')}").read(),
            )

            try:
                market_price = get_price_by_ts(
                    fork.get("name"), asset.get("name"), timestamp
                )
                asset_amount = asset_contract.functions.balanceOf(
                    fork.get("treasury_address")
                ).call(block_identifier=block) / math.pow(10, 18)
            except:
                continue

            treasury_rows.append(
                [
                    asset.get("name"),
                    block,
                    timestamp,
                    market_price * asset_amount,
                    market_price,
                    asset_amount,
                ]
            )

        treasury_data.writerows(treasury_rows)

    with open(f"{data_dir}/{fork.get('name')}/{fork.get('name')}_bonds.csv", "a+") as f:
        bond_data = csv.writer(f)
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
                        bond_contract.functions.bondPrice().call(
                            block_identifier=block
                        ),
                    ]
                    + bond_contract.functions.adjustment().call(block_identifier=block)
                    + terms
                )
            except:
                continue

        bond_data.writerows(bond_rows)
