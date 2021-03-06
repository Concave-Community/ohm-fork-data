from datetime import datetime

from stable_farm_data.annotation import auto_str


@auto_str
class Pool:
    def __init__(self, platform, name, daily_apy, weekly_apy, monthly_apy, total_apy, volume):
        self.platform = platform
        self.pool_name = name
        self.daily_apy = daily_apy
        self.weekly_apy = weekly_apy
        self.monthly_apy = monthly_apy
        self.total_apy = total_apy
        self.volume = volume
        self.snapshot_timestamp = datetime.today().strftime('%Y-%m-%d')
