from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s %(message)s')


class CAlarmDataOutput:
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
