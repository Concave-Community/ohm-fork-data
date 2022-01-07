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

### Get snapshot data
Assumes you are still in poetry shell from above.


```sh
python ohm_fork_data/get_snapshot.py
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
