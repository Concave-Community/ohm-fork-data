import time
import pytest
import os
from ohm_fork_data.get_price import get_price_by_ts


@pytest.fixture(autouse=True)
def test_build_csv():
    price = get_price_by_ts("testing", "bitcoin", 1638132591)


def test_older_timestamp():
    price = get_price_by_ts("testing", "bitcoin", 1635540617)
    assert price == 54956.84448226395


def test_existing_timestamp():
    price = get_price_by_ts("testing", "bitcoin", 1639428640)
    assert price == 46726.38660846091


def test_current_timestamp():
    price = get_price_by_ts("testing", "bitcoin", 1640724701)
    assert price == 47865.53302839184
