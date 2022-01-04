# ohm-fork-data

## Requirements

- Install Python 3.8
- Install Poetry

## Setup

```sh
git clone https://github.com/Concave-Community/ohm-fork-data
cd ohm-fork-data
poetry install
poetry shell
```

## Get snapshot data
Assumes you are still in poetry shell from above.


```sh
python ohm_fork_data/get_snapshot.py
```

## Get historical data
Assumes you are still in poetry shell from above.


```sh
python ohm_fork_data/get_data.py
```