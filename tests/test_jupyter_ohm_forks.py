import pandas as pd
import yaml
from jupyter_ohm_forks.coingecko import add_coingecko_data
from jupyter_ohm_forks.defi_llama import add_defi_llama_data
from jupyter_ohm_forks.on_chain import add_on_chain_data

def test_coingecko():

    req_columns = [
        "name",
        "token_ticker",
        "token_contract",
        "staked_ticker",
        "staked_contract",
        "staking_contract",
        "supply_contract",
        "token_abi",
        "staked_abi",
        "staking_abi",
        "supply_abi",
        "initial_index",
        "initial_supply",
        "api",
        "cg_id",
        "cg_symbol",
        "cg_name",
        "cg_image",
        "cg_current_price",
        "cg_market_cap",
        "cg_market_cap_rank",
        "cg_fully_diluted_valuation",
        "cg_total_volume",
        "cg_high_24h",
        "cg_low_24h",
        "cg_price_change_24h",
        "cg_price_change_percentage_24h",
        "cg_market_cap_change_24h",
        "cg_market_cap_change_percentage_24h",
        "cg_circulating_supply",
        "cg_total_supply",
        "cg_max_supply",
        "cg_ath",
        "cg_ath_change_percentage",
        "cg_ath_date",
        "cg_atl",
        "cg_atl_change_percentage",
        "cg_atl_date",
        "cg_roi",
        "cg_last_updated",
    ]

    with open('forks.yaml') as f:
        df1 = pd.json_normalize(yaml.load(f, Loader=yaml.SafeLoader))
    df2 = add_coingecko_data(df1)
    columns = list(df2.columns)
    columns.sort()
    req_columns.sort()
    assert columns == req_columns
    assert len(df1) == len(df2)

def test_defi_llama():
    req_columns = [
        "name",
        "token_ticker",
        "token_contract",
        "staked_ticker",
        "staked_contract",
        "staking_contract",
        "supply_contract",
        "token_abi",
        "staked_abi",
        "staking_abi",
        "supply_abi",
        "initial_index",
        "initial_supply",
        "api",
        "dl_id",
        "dl_name",
        "dl_address",
        "dl_symbol",
        "dl_url",
        "dl_description",
        "dl_chain",
        "dl_logo",
        "dl_audits",
        "dl_audit_note",
        "dl_gecko_id",
        "dl_cmcId",
        "dl_category",
        "dl_chains",
        "dl_module",
        "dl_twitter",
        "dl_audit_links",
        "dl_oracles",
        "dl_slug",
        "dl_tvl",
        "dl_chainTvls",
        "dl_change_1h",
        "dl_change_1d",
        "dl_change_7d",
        "dl_staking",
        "dl_fdv",
        "dl_mcap",
        "dl_forkedFrom",
        "dl_pool2",
        "dl_listedAt",
        "dl_audit",
        "dl_audits_link",
    ]

    with open('forks.yaml') as f:
        df1 = pd.json_normalize(yaml.load(f, Loader=yaml.SafeLoader))
    df2 = add_defi_llama_data(df1)
    columns = list(df2.columns)
    columns.sort()
    req_columns.sort()
    assert columns == req_columns
    assert len(df1) == len(df2)

def test_on_chain():

    req_columns = [
        "name",
        "token_ticker",
        "token_contract",
        "staked_ticker",
        "staked_contract",
        "staking_contract",
        "supply_contract",
        "token_abi",
        "staked_abi",
        "staking_abi",
        "supply_abi",
        "initial_index",
        "initial_supply",
        "api",
        "oc_current_block",
        "oc_epoch",
        "oc_index",
        "oc_market_cap",
        "oc_market_price",
        "oc_staking_ratio",
        "oc_staking_rebase",
        "oc_staking_tvl",
        "oc_total_supply",
        "oc_token_ticker",
        "oc_five_day_rate",
        "oc_staking_apy",
        "oc_next_rebase"
    ]

    with open('forks.yaml') as f:
        df1 = pd.json_normalize(yaml.load(f, Loader=yaml.SafeLoader))
    df2 = add_on_chain_data(df1)
    columns = list(df2.columns)
    columns.sort()
    req_columns.sort()
    assert columns == req_columns
    assert len(df1) == len(df2)