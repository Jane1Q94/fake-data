import json

from flask import Flask, request
from concurrent.futures import ThreadPoolExecutor
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
import logging
import faker
import uuid
import random
import datetime
import time
import queue

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s: %(message)s')

app = Flask(__name__)
faker = faker.Faker()


@app.route("/update/network", methods=["POST"])
def update_network():
    network = request.json.get("network")
    if network:
        GenerateData.network = network
    return {
        "network": GenerateData.network
    }


@app.route("/update/delay", methods=["POST"])
def update_delay():
    endpoint = request.json.get("endpoint")
    delay = request.json.get("delay")
    if endpoint and delay:
        list_endpoint = endpoint.split("@")
        GenerateData.config[list_endpoint[0]][list_endpoint[1]][list_endpoint[2]]["delay"] = delay
        return {
            "delay": GenerateData.config[list_endpoint[0]][list_endpoint[1]][list_endpoint[2]]["delay"]
        }
    return {
        "警告": "没有做任何改变"
    }


@app.route("/update/error", methods=["POST"])
def update_error():
    endpoint = request.json.get("endpoint")
    error = request.json.get("error")
    if endpoint and error:
        list_endpoint = endpoint.split("@")
        GenerateData.config[list_endpoint[0]][list_endpoint[1]][list_endpoint[2]]["error"] = error
        return {
            "error": GenerateData.config[list_endpoint[0]][list_endpoint[1]][list_endpoint[2]]["error"]
        }
    return {
        "警告": "没有做任何改变"
    }


@app.route("/update/traces/del", methods=["POST"])
def update_traces_del():
    trace = GenerateData.traces.pop(0)
    GenerateData.del_traces.append(trace)
    return {
        "num": len(GenerateData.traces),
        "traces": GenerateData.traces
    }


@app.route("/update/config/add", methods=["POST"])
def update_config_add():
    server_ins_num = request.json.get("serverInsNum", 10)  # 每个服务的实例的数量
    server_endpoint_num = request.json.get("serverEndPointNum", 10)  # 每个实例端点的数量
    GenerateData.config[faker.bs()] = {
        faker.ipv4(): {faker.uri_path(4): {"delay": [10, 150], "error": [100, 1]} for _ in
                       range(int(server_endpoint_num))} for _ in range(int(server_ins_num))}
    return GenerateData.config


@app.route("/update/traces/add", methods=["POST"])
def update_traces_add():
    if GenerateData.del_traces:
        trace = GenerateData.del_traces.pop(0)
        GenerateData.traces.insert(0, trace)
    else:
        trace = []
        servers = list(GenerateData.config.keys())  # 获取所有的服务
        while servers:  # trace 的长度为所有的服务长度
            server = random.choice(servers)  # 随机选择某个服务
            servers.remove(server)  # 将该服务从服务列表中删除，表示这个服务节点已经执行过，不需要再次执行
            ins = random.choice(list(GenerateData.config[server].keys()))  # 随机选取该服务下的某个实例
            endpoint = random.choice(list(GenerateData.config[server][ins].keys()))  # 随机选取该实例下的某个端点
            trace.append("%s@%s@%s" % (server, ins, endpoint))  # 服务@实例@端点 组装成一个 span
        GenerateData.traces.append(trace)
    return {
        "num": len(GenerateData.traces),
        "traces": GenerateData.traces
    }


@app.route("/output", methods=["POST"])
def output():
    address = request.json.get("address")
    topic = request.json.get("topic")
    GenerateData.pool.submit(GenerateData.output, address, topic)
    return {
        "res": "success"
    }


@app.route("/restart", methods=["POST"])
def restart():
    GenerateData.flag = True
    return {
        "res": "success"
    }


@app.route("/start", methods=["POST"])
def start():
    GenerateData.pool.submit(GenerateData.start)
    return {
        "res": "success"
    }


@app.route("/stop", methods=["POST"])
def stop():
    """
    停止实时数据
    """
    exp = request.json.get("exp", "1==1")
    GenerateData.pool.submit(GenerateData.stop, exp)
    return {
        "res": "success"
    }


@app.route("/generate/traces", methods=["POST"])
def generate_traces():
    traces = request.json.get("traces")
    if traces:
        GenerateData.traces = traces
    else:
        GenerateData.traces = []
        trace_num = request.json.get("traceNum", 10)  # 生成 X 个 trace
        # 生成 X 个 trace 的过程
        list_servers = list(GenerateData.config.keys())  # 获取所有的服务
        # weights = [trace_num for _ in range(len(list_servers))]
        while trace_num:
            span_num = random.randint(5, 7)
            trace = []
            while span_num:  # trace 的长度为所有的服务长度
                server = random.choice(list_servers)  # 随机选择某个服务
                list_servers.remove(server)  # 将该服务从服务列表中删除，表示这个服务节点已经执行过，不需要再次执行
                ins = random.choice(list(GenerateData.config[server].keys()))  # 随机选取该服务下的某个实例
                endpoint = random.choice(list(GenerateData.config[server][ins].keys()))  # 随机选取该实例下的某个端点
                trace.append("%s@%s@%s" % (server, ins, endpoint))  # 服务@实例@端点 组装成一个 span
                span_num -= 1
            GenerateData.traces.append(trace)
            trace_num -= 1
    logging.debug(GenerateData.traces)
    return {
        "num": len(GenerateData.traces),
        "traces": GenerateData.traces
    }


@app.route("/get/traces", methods=["GET"])
def get_traces():
    return {
        "num": len(GenerateData.traces),
        "traces": GenerateData.traces
    }


@app.route("/get/config", methods=["GET"])
def get_config():
    return GenerateData.config


@app.route("/generate/config", methods=["POST"])
def generate_config():
    """
    开始数据模拟
    """
    config = request.json.get("config")
    if config:
        GenerateData.config = config
    else:
        server_num = request.json.get("serverNum", 10)  # 服务的数量
        server_ins_num = request.json.get("serverInsNum", 10)  # 每个服务的实例的数量
        server_endpoint_num = request.json.get("serverEndPointNum", 10)  # 每个实例端点的数量
        logging.debug({
            "serverNum": server_num,
            "serverIns": server_ins_num,
            "serverEndpoint": server_endpoint_num,
        })

        GenerateData.config = {
            faker.bs(): {faker.ipv4(): {faker.uri_path(4): {"delay": [10, 150], "error": [100, 1]} for _ in
                                        range(int(server_endpoint_num))} for _ in range(int(server_ins_num))} for _ in
            range(int(server_num))}  # 默认每个端点的执行时间在 10~150ms之间，错误率在 1%
    return GenerateData.config


@app.route("/get/speed", methods=["GET"])
def get_speed():
    start_num = GenerateData.num
    time.sleep(1)
    end_num = GenerateData.num
    return {
        "speed": end_num - start_num
    }


@app.route("/update/speed", methods=["POST"])
def update_speed():
    speed = int(request.json.get("speed", 1000))
    GenerateData.queue_data.maxsize = speed
    return {
        "speed": GenerateData.queue_data.maxsize
    }


class GenerateData:
    flag = True  # 控制实时数据的启停
    config = {}  # 数据从配置中生成，改变配置，即改变数据
    traces = []  # 保存生成的 trace
    del_traces = []  # network delay
    network = [100, 150]  # 网络延迟
    pool = ThreadPoolExecutor()  # 线程池
    num = 0  # 已产生的数据总量
    queue_data = queue.Queue(maxsize=100)

    @classmethod
    def datetime2timestamp(cls, start_time):
        t = start_time.timetuple()
        timestamp = int(time.mktime(t) * 1000.0 + start_time.microsecond / 1000.0)
        return timestamp

    @classmethod
    def output(cls, address, topic):
        kafka = None
        if address:
            kafka = Kafka(address)
            try:
                kafka.create_topic(topic)
            except Exception as e:
                logging.info("创建kafka topic 失败：%s" % topic)
        while cls.flag:
            msg = cls.queue_data.get()
            if kafka:
                kafka.send(topic, msg)
                time.sleep(0.01)
            else:
                print(msg)

    @classmethod
    def stop(cls, exp):
        while True:
            if eval(exp):
                cls.flag = False
                break
            time.sleep(0.001)

    @classmethod
    def start(cls):
        while True:
            trace = random.choice(cls.traces)  # 随机选取一个 trace
            traceId = uuid.uuid4().hex  # 生成 traceId

            data_time = 0
            for key, value in enumerate(trace):  # 每个trace有 X 个span，这里组装每个span
                d = {
                    "traceId": traceId
                }
                if key == 0:  # 第一个 span 的开始时间
                    data_time = cls.datetime2timestamp(datetime.datetime.now())
                else:
                    data_time += random.randint(*cls.network)  # 非第一个span的开始时间要在第一个span之后，经过一段时间的网络传输

                value = value.split("@")
                d["serviceName"] = value[0]
                d["serviceInstanceName"] = value[0] + "@" + value[1]
                d["spanId"] = d["traceId"] + "_" + str(key)
                d["parentSpanId"] = d["traceId"] + "_" + str(key - 1)
                d["endpoint"] = value[2]
                d["isError"] = \
                    random.choices([False, True], weights=cls.config[value[0]][value[1]][value[2]]["error"], k=1)[0]
                d["type"] = "whole"
                d["startTime"] = data_time
                d["endTime"] = d["startTime"] + random.randint(*cls.config[value[0]][value[1]][value[2]]["delay"])
                d["language"] = "JAVA"
                d["instanceIp"] = value[1]
                d["instanceHostname"] = value[1]
                d["instanceProcessNo"] = str(random.randint(0, 65535))
                d["instanceOSName"] = "Linux"
                d["tags"] = '[{"http.method": "GET"}]'
                d["logs"] = '[{"http.method": "GET"}]'
                cls.num += 1
                cls.queue_data.put(d)
                # 如果发生调用错误，就不再往下继续了
                if d["isError"]:
                    break


class Kafka:
    def __init__(self, address):
        self.client = KafkaAdminClient(bootstrap_servers=address, client_id='%s' % (uuid.uuid1()))

        self.producer = KafkaProducer(bootstrap_servers=address,
                                      value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'),
                                      acks=0)

    def create_topic(self, topic_name, partitions=1, replication=1):
        try:
            list_topic = [NewTopic(name=topic_name, num_partitions=partitions, replication_factor=replication)]
            self.client.create_topics(new_topics=list_topic, validate_only=False)
        except Exception as e:
            logging.warning(e)

    def send(self, topic_name, data):
        try:
            self.producer.send(topic_name, data)
        except Exception as e:
            logging.error('send data to kafka failed\n%s\n%s' % (e, data))


if __name__ == '__main__':
    app.run(debug=False)
