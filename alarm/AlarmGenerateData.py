import json
import random
import datetime
import time
import pandas as pd
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from faker import Faker

fk = Faker()


class CAlarmGetData:
    q = Queue()
    list_random_alarm = [fk.sentence(random.randint(8, 14)) for _ in range(40)]
    list_root_cause_alarm = [
        "zabbix,Linux Used disk space is more than 95% on volume /oracle,Used disk space on /oracle (percentage):100 %,PROBLEM."
    ]
    list_efficient_alarm = [
        "zabbix,Oracle_instance oracle is down,oracle status on oracle:0,PROBLEM.",
    ]
    list_infect_infrastructure_alarm = [
        "zabbix,Linux CPU util > 85%,CPU util:95 %,PROBLEM.",
        "zabbix,Linux memory used > 80%,Used memory (percentage):90 %,PROBLEM."
    ]
    list_infect_transaction_alarm = [
        "zabbix,组合转账(20200930)平均处理时间连续1分钟超过100ms,20200930_transAvgProcTime:350.143,PROBLEM.",
        "zabbix,组合转账(20200930)交易成功率连续1分钟小于90%,20200930_tecSuccRate:85.43 %,PROBLEM."
    ]

    @staticmethod
    def datetime2timestamp(start_time):
        t = start_time.timetuple()
        timestamp = int(time.mktime(t) * 1000.0 + start_time.microsecond / 1000.0)
        return timestamp

    @classmethod
    def send_data_to_queue(cls, p_str_start_datetime, p_str_end_datetime, p_str_application, p_list_severity,
                           p_list_host, p_list_alarms, p_int_interval=60):

        start_datetime = datetime.datetime.strptime(p_str_start_datetime, "%Y-%m-%d %H:%M:%S")
        end_datetime = datetime.datetime.strptime(p_str_end_datetime, "%Y-%m-%d %H:%M:%S")
        interval = datetime.timedelta(seconds=p_int_interval)

        while start_datetime < end_datetime:
            for host in p_list_host:
                dict_alarm = {
                    "timestamp": cls.datetime2timestamp(start_datetime),
                    "severity": random.choice(p_list_severity),
                    "content": random.choice(p_list_alarms),
                    "application": p_str_application,
                    "host": host,
                    "code": "0001",
                    "extra": "补充字段"
                }
                cls.q.put(dict_alarm)

            start_datetime += interval

    @classmethod
    def data_output(cls):
        time.sleep(1)
        list_dict = []
        while not cls.q.empty():
            dict_alarm = cls.q.get()
            list_dict.append(dict_alarm)

        df = pd.DataFrame(list_dict)
        df = df.sort_values(by="timestamp", axis=0)
        df.to_csv("result.csv", index=None)

    @classmethod
    def main(cls):
        with open("config.json", "r", encoding="utf-8") as f:
            dict_config = json.load(f)

        list_futures = []
        with ThreadPoolExecutor(max_workers=6) as tp:
            for data_name, dict_param in dict_config.items():
                list_data = getattr(cls, data_name)
                list_futures.append(tp.submit(cls.send_data_to_queue, **dict_param, p_list_alarms=list_data))
            list_futures.append(tp.submit(cls.data_output))

        for futures in list_futures:
            futures.add_done_callback(print)


if __name__ == '__main__':
    CAlarmGetData.main()
