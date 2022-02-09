import json

import requests

from models.curve_factory_meta_pool import CurveFactoryMetaPool
from stable_farm_data.Pool import Pool


def fetch_curve_apy_volume():
    URL = "https://stats.curve.fi/raw-stats/apys.json"
    apy_volumn = requests.get(URL).json()
    daily_apy_dict = apy_volumn['apy']['day']
    weekly_apy_dict = apy_volumn['apy']['week']
    monthly_apy_dict = apy_volumn['apy']['month']
    total_apy_dict = apy_volumn['apy']['total']
    volume_dict = apy_volumn['volume']
    pools = []

    for key in daily_apy_dict:
        daily_apy = daily_apy_dict[key]
        weekly_apy = weekly_apy_dict[key]
        monthly_apy = monthly_apy_dict[key]
        total_apy = total_apy_dict[key]
        volume = volume_dict.get(key, 0)
        curve_pool = Pool(platform="Curve", name=key, daily_apy=daily_apy, weekly_apy=weekly_apy,
                          monthly_apy=monthly_apy, total_apy=total_apy, volume=volume)
        pools.append(curve_pool)
    return pools


def fetch_convex_apy_volume():
    curve_base_apy_url = "https://www.convexfinance.com/api/curve-apys"
    curve_base_apy_url = requests.get(curve_base_apy_url).json()


def json_deserialize(json_data, obj):
    py_data = json.loads(json_data)
    dic2class(py_data, obj)


def dic2class(py_data, obj):
    for name in [name for name in dir(obj) if not name.startswith('_')]:
        if name not in py_data:
            setattr(obj, name, None)
        else:
            value = getattr(obj, name)
            setattr(obj, name, set_value(value, py_data[name]))


def set_value(value, py_data):
    if str(type(value)).__contains__('.'):
        # value 为自定义类
        dic2class(py_data, value)
    elif str(type(value)) == "<class 'list'>":
        # value为列表
        if value.__len__() == 0:
            # value列表中没有元素，无法确认类型
            value = py_data
        else:
            # value列表中有元素，以第一个元素类型为准
            child_value_type = type(value[0])
            value.clear()
            for child_py_data in py_data:
                child_value = child_value_type()
                child_value = set_value(child_value, child_py_data)
                value.append(child_value)
    else:
        value = py_data
    return value


def fetch_curve_factory_pool():
    curve_base_pool_url = "https://api.curve.fi/api/getFactoryV2Pools"
    curve_base_apy_url = "https://api.curve.fi/api/getFactoryAPYs?version=2"
    pool_response = requests.get(curve_base_pool_url).json()
    apy_response = requests.get(curve_base_apy_url).json()
    pool_datas = pool_response['data']['poolData']
    apy_data = apy_response['data']['poolDetails']
    pools = []
    for pool_data in pool_datas:
        for pool_apy in apy_data:
            if pool_data['address'] == pool_apy['poolAddress']:
                pool = CurveFactoryMetaPool(pool_data, pool_apy)
                pools.append(pool)
                print(pool)

    return pools


if __name__ == '__main__':
    fetch_curve_factory_pool()
