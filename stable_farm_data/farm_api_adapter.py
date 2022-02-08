import requests

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