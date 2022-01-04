from on_chain import save_block_data
import web3
import yaml

with open("forks.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)

abi_dir = config.get("abi_dir", "./abi")
data_dir = config.get("data_dir", "./data")
moralis_key = config.get("moralis_key")

for chain in config.get("chains"):
    chain_name = chain.get("name")
    endpoint = chain.get("archive")
    step = float(chain.get("step", "5e5"))

    # get current block
    w3 = web3.Web3(web3.Web3.HTTPProvider(endpoint))
    current_block = w3.eth.get_block_number()

    for fork in chain.get("forks", None):
        fork_name = fork.get("name")
        end_block = int(fork.get("end_block"))
        start_block = int(fork.get("start_block"))

        # single get
        if end_block != start_block:
            end_block == current_block
            endpoint = chain.get("endpoint")

        while end_block <= current_block:

            save_block_data(
                fork, chain_name, end_block, endpoint, abi_dir, data_dir, moralis_key
            )
            fork["end_block"] = end_block
            end_block = int(step + end_block)

with open("forks.yaml", "w") as f:
    yaml.dump(config, f)
