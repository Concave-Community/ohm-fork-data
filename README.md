# ohm-fork-data

## Requirements

- Install Python 3.8
- Install Poetry

## Setup (without Docker)

```sh
git clone https://github.com/Concave-Community/ohm-fork-data
cd ohm-fork-data
poetry install
poetry shell
```

### Get snapshot data for forks
Assumes you are still in poetry shell from above.

```sh
python ohm_fork_data/get_snapshot.py
```

### Get Farm Data 
Now only support curve - 3pool, but more is on the way
```shell
python stable_farm_data/get_curve_snapshot.py
```


### Get historical data
Assumes you are still in poetry shell from above.


```sh
python ohm_fork_data/get_data.py
```

## Setup (with Docker)
### Pre-requisite
1. docker
2. docker-compose

### Install Snapshot data
```shell
docker-compose build && docker-compose up snapshot-data
```

### Install Historic data
```shell
docker-compose build && docker-compose up historic-data
```
