import math
from GdsConfig import CGdsConfig


class CGdsTs:
    @classmethod
    def calc_current(cls, _datetime, noise):
        """
        计算某个时间点的并发量
        """
        time = _datetime.hour * 60 * 60 + _datetime.minute * 60 + _datetime.second
        x = math.pi / (24 * 60 * 60) * time
        return CGdsConfig.model(x, noise)
