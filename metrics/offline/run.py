import json
import math
import logging
import datetime
import random
import time

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s: %(message)s')


class FakerOfflineTemplate:
    def __init__(self, apps, start_datetime, end_datetime, time_interval, data_output):
        self.data_output = data_output
        self.interval = time_interval
        self.apps = apps
        self.start_time = start_datetime
        self.end_time = end_datetime
        self.status = True
        if data_output.get("print"):
            pass
        else:
            self.create_database(data_output)

    def set_apps(self, apps):
        self.apps = apps

    @staticmethod
    def create_database(data_output):
        kafka_server = data_output.get("kafka_server")
        es_server = data_output.get("es_server")
        database = data_output.get("database")
        es_config = data_output.get("config").get("es")
        kafka_config = data_output.get("config").get("kafka")

        if es_server:
            try:
                es = Elasticsearch(es_server)
                es.indices.create(index=database, body=es_config)
            except Exception as e:
                logging.error("创建es index 失败，失败的原因为\n%s" % e)

        if kafka_server:
            client = KafkaAdminClient(bootstrap_servers=kafka_server)
            replication = kafka_config.get("replication", 1)
            partition = kafka_config.get("partition", 1)
            topic_list = [NewTopic(name=database, num_partitions=partition, replication_factor=replication)]
            try:
                client.create_topics(new_topics=topic_list, validate_only=False)
            except Exception as e:
                logging.error("创建 kafka topic 失败，失败的原因为\n%s" % e)

    @staticmethod
    def insert_data(data_output, data):
        kafka_server = data_output.get("kafka_server")
        es_server = data_output.get("es_server")
        database = data_output.get("database")

        # send data
        if es_server:
            try:
                es = Elasticsearch(es_server)
                bulk(es, data, index=database, raise_on_error=True)
            except Exception as e:
                logging.error("插入 ES 数据失败，失败的原因为\n%s" % e)

        if kafka_server:
            producer = KafkaProducer(bootstrap_servers=kafka_server, api_version=(0, 11, 5),
                                     value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'),
                                     acks=0)
            try:
                for d in data:
                    producer.send(database, d)
                producer.close()
            except Exception as e:
                logging.error("插入 kafka 数据失败，失败的原因为\n%s" % e)

    @staticmethod
    def datetime2timestamp(start_time):
        t = start_time.timetuple()
        timestamp = int(time.mktime(t) * 1000.0 + start_time.microsecond / 1000.0)
        return timestamp

    @staticmethod
    def normalize(value, _min, _max, factor):
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

    @staticmethod
    def period_transaction_func(x, noise):
        _time = x.hour * 60 * 60 + x.minute * 60 + x.second
        x = math.pi / (24 * 60 * 60) * _time
        value = math.fabs(math.sin(x)) + math.fabs(math.sin(2 * x)) + random.gauss(0, noise)
        return value

    @staticmethod
    def period_machine_func(x, noise):
        _time = x.hour * 60 * 60 + x.minute * 60 + x.second
        x = math.pi / (24 * 60 * 60) * _time
        x = 0.52 + (2.63 - 0.52) / math.pi * x
        return math.fabs(math.sin(x)) + math.fabs(math.sin(2 * x)) + math.fabs(math.sin(3 * x)) + math.fabs(
            math.sin(4 * x)) + random.gauss(0, noise)

    def run(self):
        list_data = []
        start_datetime = datetime.datetime.strptime(self.start_time, "%Y-%m-%d %H:%M:%S")
        end_datetime = datetime.datetime.strptime(self.end_time, "%Y-%m-%d %H:%M:%S")
        time_interval = datetime.timedelta(seconds=random.choice(self.interval))
        while start_datetime < end_datetime:
            dict_data = {}
            for app in self.apps:
                # dict_data = {}
                app_name = app.get("name")
                dict_data["name"] = app_name
                metrics = app.get("metrics")
                dict_data["timestamp"] = self.datetime2timestamp(start_datetime)
                for m in metrics:
                    t = m.get("type")
                    factor = float(m.get("factor"))
                    metric_name = m.get("name")
                    noise = float(m.get("noise", 0.14))
                    if t == "transaction":
                        dict_data[metric_name] = self.normalize(self.period_transaction_func(start_datetime, noise), 0, 1.76017,
                                                                factor)
                    elif t == "machine":
                        dict_data[metric_name] = self.normalize(self.period_machine_func(start_datetime, noise), 0, 3.23238,
                                                                factor)
                # list_data.append(dict_data)
            list_data.append(dict_data)
            start_datetime = start_datetime + time_interval
        if self.data_output.get("print"):
            logging.info("%s" % list_data)
        else:
            self.insert_data(self.data_output, list_data)


if __name__ == '__main__':
    # with open("apps-abnormal.json", 'r', encoding='utf-8') as f:
    #     dict_apps = json.load(f)
    #     list_apps = dict_apps.get('apps')
    with open("apps-normal.json", 'r', encoding='utf-8') as f:
        dict_apps = json.load(f)
        list_apps = dict_apps.get('apps')

    # with open("debugDataOutput.json", 'r', encoding='utf-8') as f:
    #     dict_apps = json.load(f)
    #     dict_data_output = dict_apps
    with open("dataOutput.json", 'r', encoding='utf-8') as f:
        dict_apps = json.load(f)
        dict_data_output = dict_apps

    interval = [300]
    # start = "2021-06-01 00:00:00"
    # end = "2021-06-15 13:30:00"

    # start = "2021-06-15 13:30:00"
    # end = "2021-06-15 14:30:00"

    start = "2021-06-15 14:30:00"
    end = "2021-07-09 11:30:00"

    c_data = FakerOfflineTemplate(list_apps, start, end, interval, dict_data_output)
    c_data.run()
