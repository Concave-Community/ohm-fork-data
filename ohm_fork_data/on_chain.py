import web3
import requests
import yaml
import csv
import math


def get_market_price(fork, timestamp):
    # TODO - find an API to get price based on timestamp
    return 100


def save_block_data(fork, chain, block, endpoint, abi_dir, data_dir):
    w3 = web3.Web3(web3.Web3.HTTPProvider(endpoint))

    # avax requires special middleware
    if chain == "avax":
        w3.middleware_onion.inject(web3.middleware.geth_poa_middleware, layer=0)

    timestamp = w3.eth.get_block(block).timestamp
    market_price = get_market_price(fork.get('name'), timestamp)

    with open(f"{data_dir}/{fork.get('name')}.csv", "a+") as f:
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
        if fork == "time":
            epoch = [epoch[1], epoch[3], epoch[0], epoch[2]]

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
                market_price
            ]
            + epoch[:-1]
            + [epoch[3] / math.pow(10, 9)]
        )

        fork_data.writerow(fork_row)

    return

    # TODO - finish off the bond data based on input from XD
    with open(f"{data_dir}/{fork.get('name')}bonds.csv", "a+") as f:
        bond_data = csv.writer(f)
        bond_rows = []

        for bond in fork.get("bonds"):
            bond_contract = w3.eth.contract(
                web3.Web3.toChecksumAddress(bond.get("address")),
                abi=open(f"{abi_dir}/{fork.get('bond_abi')}").read(),
            )

            bond_row = (
                [
                    bond.get("name"),
                    block,
                    bond_contract.functions.bondPrice().call(block_identifier=block),
                ]
                + bond_contract.functions.adjustment().call(block_identifier=block)
                + bond_contract.functions.terms().call(block_identifier=block)
            )

        bond_data.writerows(bond_rows)
