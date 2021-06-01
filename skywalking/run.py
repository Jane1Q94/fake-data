from flask import Flask, request
import logging
import faker
import uuid
import random
import datetime
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s: %(message)s')

app = Flask(__name__)
faker = faker.Faker()

# 数据从配置中生成，改变配置，即改变数据
config = {}

# 保存生成的 trace
traces = []

flag = True


@app.route("/start", methods=["POST"])
def start():
    global config
    global traces
    server_num = request.json.get("serverNum")
    server_ins_num = request.json.get("serverInsNum")
    server_endpoint_num = request.json.get("serverEndPointNum")
    trace_num = request.json.get("traceNum")
    logging.debug({
        "serverNum": server_num,
        "serverIns": server_ins_num,
        "serverEndpoint": server_endpoint_num,
        "traceNum": trace_num
    })

    if not (server_num and server_ins_num and server_endpoint_num and trace_num):
        return {
            "错误": "缺少参数！(serverNum, serverIns, serverEndPoint, traceNum)"
        }
    config = {
        faker.bs(): {faker.ipv4(): {faker.uri_path(4): {"delay": [10, 150], "error": [100, 1]} for _ in
                                    range(int(server_endpoint_num))} for _ in range(int(server_ins_num))} for _ in
        range(int(server_num))}

    while trace_num:
        servers = list(config.keys())  # 获取所有的服务
        trace = []
        while servers:
            server = random.choice(servers)  # 随机选择某个服务
            servers.remove(server)
            ins = random.choice(list(config[server].keys()))  # 获取该服务下的实例
            endpoint = random.choice(list(config[server][ins].keys()))  # 获取该实例下的端点
            trace.append("%s@%s@%s" % (server, ins, endpoint))  # 组装成 trace
        traces.append(trace)
        trace_num -= 1
    logging.debug(traces)
    GenerateData.start()
    return {"res": "success"}


class GenerateData:
    @classmethod
    def timestamp(cls):
        now = datetime.datetime.now()
        t = now.timetuple()
        timestamp = int(time.mktime(t) * 1000.0 + now.microsecond / 1000.0)
        return timestamp

    @classmethod
    def start(cls):
        global flag
        data = []
        while flag:
            traceId = uuid.uuid4().hex
            trace = random.choice(traces)  # 随机选取一个 trace
            startTime = None
            for key, value in enumerate(trace):  # 封装 span 数据
                d = {
                    "traceId": traceId
                }
                if not startTime:
                    startTime = cls.timestamp()
                else:
                    startTime += random.randint(100, 150)
                value = value.split("@")
                d["serviceName"] = value[0]
                d["serviceInstanceName"] = value[0] + "@" + value[1]
                d["spanId"] = d["traceId"] + "_" + str(key)
                d["parentSpanId"] = d["traceId"] + "_" + str(key - 1)
                d["endpoint"] = value[2]
                d["isError"] = \
                    random.choices(["false", "true"], weights=config[value[0]][value[1]][value[2]]["error"], k=1)[0]
                d["type"] = "whole"
                d["startTime"] = startTime
                d["endTime"] = d["startTime"] + random.randint(*config[value[0]][value[1]][value[2]]["delay"])
                data.append(d)
                if len(data) >= 1000:
                    logging.debug(data)
                    flag = False
                    break


if __name__ == '__main__':
    app.run(debug=False)
