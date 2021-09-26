import math
import random


class CGdsConfig:
    server = "http://192.168.101.11:9000"

    @classmethod
    def model(cls, x, noise):
        return cls.__model_01(x, noise)

    @classmethod
    def __model_01(cls, x, noise, _min=0, _max=1.76017):
        """
        模拟时序时序，交易量类型，波动较大
        """
        value = math.fabs(math.sin(x)) + math.fabs(math.sin(2 * x)) + random.gauss(0, noise)
        value = (value - _min) / (_max - _min)
        value = value if value > 0 else 0
        return value


class CDBConfig:
    es_server = "http://192.168.101.11:9200"
    es_index_api_record = "api-monitor"
    es_api_record_flush_num = 400
    es_mapping = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "timestamp": {
                    "type": "date",
                    "format": "epoch_millis"
                }
            }
        }
    }
