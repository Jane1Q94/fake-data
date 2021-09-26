# 客户端的请求数据同步到ES后，Zabbix能够监控客户端请求数据，并且配置阈值
import json
import requests
import datetime
import sys
import psutil
from psutil import NoSuchProcess


class CGdsZabbixScript:
    url = "http://192.168.101.11:9200/api-monitor/_search"

    @classmethod
    def zabbix_client_api(cls, metric_name):
        current_datetime = datetime.datetime.utcnow()
        dict_request_body = {
            "aggs": {
                "3": {
                    "date_histogram": {
                        "field": "timestamp",
                        "interval": "1m",
                        "time_zone": "Asia/Shanghai",
                        "min_doc_count": 1
                    },
                    "aggs": {
                        "4": {
                            "terms": {
                                "field": "api.keyword",
                                "size": 10,
                                "order": {
                                    "2": "desc"
                                }
                            },
                            "aggs": {
                                "2": {
                                    "avg": {
                                        "field": "duration"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "size": 0,
            "_source": {
                "excludes": []
            },
            "stored_fields": [
                "*"
            ],
            "script_fields": {},
            "docvalue_fields": [
                {
                    "field": "timestamp",
                    "format": "date_time"
                }
            ],
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "timestamp": {
                                    "format": "strict_date_optional_time",
                                    "gte": (current_datetime - datetime.timedelta(minutes=2)).strftime(
                                        "%Y-%m-%dT%H:%M:%S.000Z"),
                                    "lte": current_datetime.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                                }
                            }
                        }
                    ],
                    "filter": [
                        {
                            "match_all": {}
                        },
                        {
                            "match_all": {}
                        }
                    ],
                    "should": [],
                    "must_not": []
                }
            }
        }
        dict_resp = requests.post(cls.url, json=dict_request_body).json()
        list_buckets_data = dict_resp.get("aggregations").get("3").get("buckets")
        if not list_buckets_data:
            print(0)
        else:
            # [{'key': 'http://192.168.101.11:9000/dgs/api/ec/order/create', 'doc_count': 825, '2': {'value': 0.33309090736463215}}]
            list_data = list_buckets_data[-1].get("4").get("buckets")
            api, metric = metric_name.split("-")
            for dict_metric in list_data:
                if api == dict_metric.get("key"):
                    if metric == "duration":
                        print(int(dict_metric.get("2").get("value") * 1000))
                    elif metric == "count":
                        print(dict_metric.get("doc_count"))

    @classmethod
    def zabbix_client_api_records(cls):
        dict_api_records = {
            "data": [
                {
                    "{#API}": "http://192.168.101.11:9000/dgs/api/ec/order/create"
                },
                {
                    "{#API}": "http://192.168.101.11:9000/dgs/api/ec/order/updatestatus"
                },
                {
                    "{#API}": "http://192.168.101.11:9000/dgs/api/ec/user/passwordlogin"
                }
            ]
        }
        print(json.dumps(dict_api_records))

    @classmethod
    def zabbix_get_process_data(cls, param):
        pid, attr = param.split(".")
        try:
            process = psutil.Process(int(pid))
            if attr == "cpu_percent":
                value = getattr(process, attr)(interval=1)
            else:
                value = getattr(process, attr)()
            print(round(float(value), 2))
        except NoSuchProcess:
            pass
        except AttributeError:
            pass


if __name__ == '__main__':
    load_method = sys.argv[1]
    if load_method == "load api list":
        CGdsZabbixScript.zabbix_client_api_records()
    elif load_method == "load api metric":
        metric_name = sys.argv[2]
        CGdsZabbixScript.zabbix_client_api(metric_name)
    elif load_method == "zabbix_get_process_data":
        param = sys.argv[2]
        CGdsZabbixScript.zabbix_get_process_data(param)
