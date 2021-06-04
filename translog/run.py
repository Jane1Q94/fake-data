""""
样例： 4684:2021040123595994:2021040100000005:16.7.33.21:Z0000004:00000
说明：
1. 交易号 4种类型
2. 开始时间
3. 结束时间
4. 客户端IP
5. 渠道号
6. 返回码
某类交易号在某个时间段内出现大量错误返回码
"""
from concurrent.futures import ThreadPoolExecutor
from elasticsearch import Elasticsearch
import datetime
import math
import random
import queue
import time


class TimeSeries:

    @classmethod
    def generate_time_data_trans(cls, _datetime, noise):
        """
        模拟时序时序，交易量类型，波动较大
        """
        time = _datetime.hour * 60 * 60 + _datetime.minute * 60 + _datetime.second
        x = math.pi / (24 * 60 * 60) * time
        value = math.fabs(math.sin(x)) + math.fabs(math.sin(2 * x)) + random.gauss(0, noise)
        return value

    @classmethod
    def generate_time_data_machine(cls, _datetime, noise):
        """
        模拟时序时序，机器指标类型，波动较小
        """
        time = _datetime.hour * 60 * 60 + _datetime.minute * 60 + _datetime.second
        x = math.pi / (24 * 60 * 60) * time
        x = 0.52 + (2.63 - 0.52) / math.pi * x
        return math.fabs(math.sin(x)) + math.fabs(math.sin(2 * x)) + math.fabs(math.sin(3 * x)) + math.fabs(
            math.sin(4 * x)) + random.gauss(0, noise)

    @classmethod
    def normalize(cls, value, _min, _max, factor):
        """
        数据规范化
        """
        value = (value - _min) / (_max - _min)
        if factor > 1:
            if value < 0:
                return 0.01 * factor
        elif factor <= 1:
            if value < 0:
                return 0.01 * factor
            if value > 1:
                return 1 * factor
            return value * factor
        return value * factor


class Generate:
    q = queue.Queue()
    pool = ThreadPoolExecutor()
    data = []

    @classmethod
    def output(cls):
        es = Elasticsearch("http://192.168.101.11:9200")
        mapping = {
            "settings": {
                "number_of_shards": 3,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "end_timestamp": {
                        "type": "date",
                    },
                    "start_timestamp": {
                        "type": "date",
                    }
                }
            }
        }
        try:
            es.indices.create("test6", body=mapping)
        except:
            pass
        while True:
            data = cls.q.get()
            data_split = data.split(":")
            dict_data = {
                "trans_code": data_split[0],
                "start_timestamp": int(data_split[1]),
                "end_timestamp": int(data_split[2]),
                "client_ip": data_split[3],
                "channel_code": data_split[4],
                "return_code": data_split[5]
            }
            print(dict_data)
            es.index(index="test6", body=dict_data)

    @classmethod
    def generate(cls, start_datetime, end_datetime, mete_data, _type="trans", factor=1000, noise=0.14, speed=100000,
                 interval=60):
        """
        模拟交易日志数据
        :param start_datetime: 开始时间, datetime 类型
        :param end_datetime: 结束时间， datetime 类型
        :param _type: 数据类型，trans 为交易类型数据，machine 为机器类型数据
        :param factor: 数据均值
        :param noise: 噪声
        :param speed：控制数据生成的速度
        :param mete_data: 元数据
        :param interval: 时间间隔
        :return:
        """
        cls.q.maxsize = speed
        start_datetime = datetime.datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")
        end_datetime = datetime.datetime.strptime(end_datetime, "%Y-%m-%d %H:%M:%S")
        second = datetime.timedelta(seconds=interval)
        while start_datetime < end_datetime:
            log_num = 0
            if _type == "trans":
                log_num = TimeSeries.generate_time_data_trans(start_datetime, noise)
                log_num = int(TimeSeries.normalize(log_num, 0, 1.76017, factor))
            elif _type == "machine":
                log_num = TimeSeries.generate_time_data_machine(start_datetime, noise)
                log_num = int(TimeSeries.normalize(log_num, 0, 3.23238, factor))
            else:
                print("_type 参数错误！")

            for _ in range(log_num):
                data = cls.__trans_log(start_datetime, mete_data)
                cls.q.put(data)
            start_datetime += second

    @classmethod
    def __trans_log(cls, _datetime, mete_data):
        """
        sample: 4684:2021040123595994:2021040100000005:16.7.33.21:Z0000004:00000
        :param _datetime:
        :param mete_data:
        :return:
        """
        keys = list(mete_data.keys())
        trans_code = random.choices(keys, weights=[1 for _ in range(len(keys))])[0]
        mete_data = mete_data.get(trans_code)
        client_ip = random.choices(mete_data.get("client_ip").get("value"),
                                   weights=mete_data.get("client_ip").get("weight"))[0]
        channel_code = random.choices(mete_data.get("channel_code").get("value"),
                                      weights=mete_data.get("channel_code").get("weight"))[0]
        return_code = random.choices(mete_data.get("return_code").get("value"),
                                     weights=mete_data.get("return_code").get("weight"))[0]
        delay_time = random.choices(mete_data.get("delay_time").get("value"),
                                    weights=mete_data.get("delay_time").get("weight"))[0]
        start_time = cls.__datetime2timestamp(_datetime)
        end_time = start_time + delay_time
        return "%s:%s:%s:%s:%s:%s" % (trans_code, start_time, end_time, client_ip, channel_code, return_code)

    @classmethod
    def __datetime2timestamp(cls, start_time):
        t = start_time.timetuple()
        timestamp = int(time.mktime(t) * 1000.0 + start_time.microsecond / 1000.0)
        return timestamp


if __name__ == '__main__':
    Generate.pool.submit(Generate.output)
    mete_data = {
        key: {
            "trans_code": {
                "value": [4684, 4989, 5894, 3745],
                "weight": [1, 1, 1, 1]
            },
            "client_ip": {
                "value": ["192.168.101.1", "192.168.101.2", "192.168.101.3", "192.168.101.4"],
                "weight": [1, 1, 1, 1]
            },
            "channel_code": {
                "value": ["Z0000001", "Z0000002", "Z0000003", "Z0000004"],
                "weight": [1, 1, 1, 1]
            },
            "return_code": {
                "value": ["00000000", "00000001"],
                "weight": [1000, 1]
            },
            "delay_time": {
                "value": [i for i in range(40, 60)],
                "weight": [1 for _ in range(20)]
            }
        } for key in [1234, 3456, 4567, 5678]}

    start_datetime = "2021-06-01 00:00:00"
    end_datetime = "2021-06-01 14:50:00"
    Generate.generate(start_datetime, end_datetime, mete_data, factor=10)

    start_datetime = "2021-06-01 14:50:00"
    end_datetime = "2021-06-01 15:00:00"
    mete_data[1234]["return_code"] = {
        "value": ["00000000", "00000001"],
        "weight": [1, 100000]
    }
    Generate.generate(start_datetime, end_datetime, mete_data, factor=10)

    start_datetime = "2021-06-01 15:00:00"
    end_datetime = "2021-06-02 00:00:00"
    mete_data[1234]["return_code"] = {
        "value": ["00000000", "00000001"],
        "weight": [1000, 1]
    }
    Generate.generate(start_datetime, end_datetime, mete_data, factor=10)
