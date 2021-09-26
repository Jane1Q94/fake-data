import functools
import json
import sys
import time
import logging

import requests

from GdsConfig import CDBConfig


class CGdsWrapper:
    """
    eoitek_gds 系统中涉及到的装饰器
    """
    __total_record = 0
    __str_record = ""

    @classmethod
    def retry(cls, count=3, desc=""):
        """
        当API返回的错误码部位None时，一直重试
        """

        def wrapper_func(func):
            @functools.wraps(func)
            async def wrapper_params(*args, **kwargs):
                inner_count = 1
                res_data, res_json = await func(*args, **kwargs)
                error_message = res_data["message"]
                while error_message:
                    if inner_count > count:
                        logging.error("%s\n%s\n[%s %s]" % (desc, res_data, res_json, kwargs))
                        raise Exception("%s retry times exceeded!" % desc)
                    res_data, res_json = await func(*args, **kwargs)
                    error_message = res_data.get("message")
                    inner_count += 1
                return res_data

            return wrapper_params

        return wrapper_func

    @classmethod
    def record_time(cls, func):
        """
        记录每次调用的时间
        """

        @functools.wraps(func)
        async def wrapper_func(*args, **kwargs):
            start = time.time()
            res_data, res_url, res_json, header = await func(*args, **kwargs)
            time_diff = time.time() - start

            assert type(res_data) is dict, "request to %s, but response is not valid" % res_data

            api_stat = {
                "timestamp": int(start * 1000),
                "api": res_url,
                "duration": round(time_diff, 2),
                "success": res_data.get("success"),
                "errorCode": res_data.get("errorCode"),
                "message": res_data.get("message"),
                "request": res_json,
                "header": header
            }
            logging.debug(api_stat)
            cls.__str_record += json.dumps({"index": {"_index": CDBConfig.es_index_api_record}}) + "\n"
            cls.__str_record += json.dumps(api_stat) + "\n"
            cls.__total_record += 1
            if cls.__total_record >= CDBConfig.es_api_record_flush_num:
                requests.post(CDBConfig.es_server + "/_bulk", data=cls.__str_record,
                              headers={"Content-Type": "application/json"}).json()
                logging.info("-" * 90 + " sync client request data to es " + "-" * 90)
                cls.__total_record = 0
                cls.__str_record = ""
            return res_data, res_json

        return wrapper_func
