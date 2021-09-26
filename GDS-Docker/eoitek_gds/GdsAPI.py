import asyncio
import copy
import json
from aiohttp import web
from concurrent import futures
from GdsEc import CGdsEc


class Handlers:
    def __init__(self):
        # api 返回的json模板
        self.dict_res = {
            "success": True,
            "errorCode": "0000",
            "message": "",
            "code": 20000,
            "data": {}
        }
        # 记录任务的状态
        self.dict_task_record = {
        }

        # 线程池
        self.thread_pool = futures.ThreadPoolExecutor()
        # 当前实现的虚拟业务列表
        self.business = {
            "ec": CGdsEc
        }
        self.run_func = {
            "ec": []
        }

    async def handler_dgs_create(self, request):
        """
        逻辑：如果任务已存在，就重启任务，否则新建任务，新建的任务提交到线程池
        """

        # 获取请求json，准备响应json
        dict_req = await request.json()
        dict_res = copy.deepcopy(self.dict_res)

        # 解析参数
        business_name = dict_req.get("business_name")
        func_name = dict_req.get("func_name")
        dict_parameters = dict_req.get("parameters", {})

        if not (business_name and func_name):
            dict_res["success"] = False
            dict_res["errorCode"] = "1001"
            dict_res["code"] = 10000
            dict_res["message"] = "request json must include <business_name、func_name>"
            return web.json_response(dict_res)

        elif self.business.get(business_name) is None:
            dict_res["success"] = False
            dict_res["errorCode"] = "1002"
            dict_res["code"] = 10000
            dict_res["message"] = "business %s is not supported" % business_name
            return web.json_response(dict_res)

        elif getattr(self.business.get(business_name), "dict_api").get("data").get(func_name) is None:
            dict_res["success"] = False
            dict_res["errorCode"] = "1003"
            dict_res["code"] = 10000
            dict_res["message"] = "api %s is invalid, please check api name" % func_name
            return web.json_response(dict_res)

        else:
            dict_api = getattr(self.business.get(business_name), "dict_api").get("data")

            for key, value in dict_parameters.items():
                if key in dict_api.keys():
                    dict_api[func_name][key] = value
                else:
                    dict_res["success"] = False
                    dict_res["errorCode"] = "1004"
                    dict_res["code"] = 10000
                    dict_res["message"] = "%s is not invalid!" % key
                    return web.json_response(dict_res)

            loop = asyncio.new_event_loop()

            with open("cache/cache.json", "r", encoding="utf-8") as f:
                dict_cache = json.load(f)
                dict_cache[business_name] = dict_api

            with open("cache/cache.json", "w", encoding="utf-8") as f:
                json.dump(dict_cache, f)

            if func_name in self.run_func[business_name]:
                pass
            else:
                func_entrypoint = getattr(self.business.get(business_name), "main")
                self.thread_pool.submit(func_entrypoint, loop, func_name)
                self.run_func[business_name].append(func_name)

        return web.json_response(dict_res)

    async def handler_dgs_info(self, request):
        # 获取请求json，准备响应json
        dict_res = copy.deepcopy(self.dict_res)
        for business_name, C_business in self.business.items():
            dict_api = getattr(C_business, "dict_api")
            dict_res["data"][business_name] = dict_api['data']
        return web.json_response(dict_res)


if __name__ == '__main__':
    handler = Handlers()
    app = web.Application()
    app.add_routes([
        web.post("/dgs/create", handler.handler_dgs_create),
        web.get("/dgs/info", handler.handler_dgs_info),
    ])
    web.run_app(app)
