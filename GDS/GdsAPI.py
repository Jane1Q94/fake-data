import asyncio
import copy
from aiohttp import web
from concurrent import futures
from GdsConfig import CDBConfig
from concurrent import futures
from GdsEc import CGdsEc


class Handlers:
    def __init__(self):
        # api 返回的json模板
        self.dict_res = {
            "success": True,
            "errorCode": "0000",
            "message": "",
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

    async def handler_dgs_start(self, request):
        """
        逻辑：如果任务已存在，就重启任务，否则新建任务，新建的任务提交到线程池
        """

        # 获取请求json，准备响应json
        dict_req = await request.json()
        dict_res = copy.deepcopy(self.dict_res)

        # 解析参数
        business_name = dict_req.get("business_name", "ec")

        # 判断业务名称是否合法，不合法直接返回错误信号
        if business_name not in self.business.keys():
            dict_res["success"] = False
            dict_res["errorCode"] = "1001"
            dict_res["message"] = "unknown business name"
            return web.json_response(dict_res)

        # 如果任务已存在，并且是 stopped 状态，就重启任务即可
        if business_name in self.dict_task_record.keys() and self.dict_task_record[business_name]["state"] == "stopped":
            setattr(self.business[business_name], "running", True)
            self.dict_task_record[business_name]["state"] = "running"
        # 如果任务不存在，就新创建一个事件循环，在独立的事件循环以及线程中运行任务
        else:
            loop = asyncio.new_event_loop()
            func_entrypoint = getattr(self.business.get(business_name), "main")
            self.thread_pool.submit(func_entrypoint, loop)
            # 记录任务状态
            self.dict_task_record[business_name] = {
                "state": "running",
                "params": {}
            }

        return web.json_response(dict_res)

    async def handler_dgs_stop(self, request):
        """
        停止正在运行的业务请求
        """

        # 获取请求json，准备响应json
        dict_req = await request.json()
        dict_res = copy.deepcopy(self.dict_res)

        # 解析参数
        business_name = dict_req.get("business_name")

        # 判断业务名称是否合法或者当前业务的状态是否是running状态，非running状态无法停止
        if business_name not in self.business.keys():
            dict_res["success"] = False
            dict_res["errorCode"] = "1001"
            dict_res["message"] = "unknown business name"
            return web.json_response(dict_res)
        elif business_name not in self.dict_task_record.keys():
            dict_res["success"] = False
            dict_res["errorCode"] = "2001"
            dict_res["message"] = "the business has never been run!"
            return web.json_response(dict_res)
        elif self.dict_task_record[business_name]["state"] != "running":
            dict_res["success"] = False
            dict_res["errorCode"] = "2002"
            dict_res["message"] = "current state of this business is not running!"
            return web.json_response(dict_res)

        # 停止当前任务
        setattr(self.business[business_name], "running", False)
        self.dict_task_record[business_name]["state"] = "stopped"

        return web.json_response(dict_res)

    async def handler_dgs_update(self, request):
        # 获取请求json，准备响应json
        dict_req = await request.json()
        dict_res = copy.deepcopy(self.dict_res)

        business_name = dict_req.get("business_name")
        # 判断业务名称是否合法或者当前业务的状态是否是running状态，非running状态无法更新参数，只有在内存中的参数才能被更新
        if business_name not in self.business.keys():
            dict_res["success"] = False
            dict_res["errorCode"] = "1001"
            dict_res["message"] = "unknown business name"
            return web.json_response(dict_res)
        elif business_name not in self.dict_task_record.keys():
            dict_res["success"] = False
            dict_res["errorCode"] = "2001"
            dict_res["message"] = "the business has never been run!"
            return web.json_response(dict_res)
        elif self.dict_task_record[business_name]["state"] != "running":
            dict_res["success"] = False
            dict_res["errorCode"] = "2002"
            dict_res["message"] = "current state of this business is not running!"
            return web.json_response(dict_res)

        list_req_params = [p for p in dict_req.keys() if p != "business_name"]

        for p in list_req_params:
            try:
                if p == "speed":
                    CDBConfig.es_api_record_flush_num = dict_req[p] * 40  # 修改发送数据的阈值
                    origin_speed = getattr(self.business[business_name], "speed")  # 请求数变多后，相应的错误数应该也要相应增加
                    ratio = int((dict_req[p] / origin_speed) ** 3)  # 用幂是为了保证当倍数为 1 时，错误比例不会增加

                    setattr(self.business[business_name], "list_func_weights", [ratio, 100])  # 更新错误比例
                getattr(self.business[business_name], p)
                setattr(self.business[business_name], p, dict_req[p])
                self.dict_task_record[business_name]["params"][p] = dict_req[p]
            except AttributeError as e:
                dict_res["success"] = False
                dict_res["errorCode"] = "1001"
                dict_res["message"] = "%s is an invalid parameter" % p
                return web.json_response(dict_res)

        return web.json_response(dict_res)

    async def handler_dgs_query(self, request):
        # 获取请求json，准备响应json
        dict_res = copy.deepcopy(self.dict_res)
        dict_res["data"] = self.dict_task_record
        return web.json_response(dict_res)

    async def handler_dgs_info(self, request):
        # 获取请求json，准备响应json
        dict_res = copy.deepcopy(self.dict_res)
        for business_name, C_business in self.business.items():
            business_stats = getattr(C_business, "dict_stats")
            dict_res["data"][business_name] = business_stats
        return web.json_response(dict_res)


if __name__ == '__main__':
    handler = Handlers()
    app = web.Application()
    app.add_routes([
        web.post("/dgs/start", handler.handler_dgs_start),
        web.post("/dgs/stop", handler.handler_dgs_stop),
        web.post("/dgs/update", handler.handler_dgs_update),
        web.get("/dgs/query", handler.handler_dgs_query),
        web.get("/dgs/info", handler.handler_dgs_info),
    ])
    web.run_app(app)

