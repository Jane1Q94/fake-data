import asyncio
import datetime
import random
import aiohttp
from GDS import logging
from GdsTs import CGdsTs
from GdsAReq import CGdsAReq
from GdsConfig import CGdsConfig
from GdsWrapper import CGdsWrapper
from concurrent import futures


class CGdsEc:
    running = True
    list_str_func = ["login_passwd_error", "pay_order_normal"]
    list_func_weights = [1, 100]
    speed = 40
    noise = 0.2

    query_order_api = CGdsConfig.server + "/dgs/api/ec/orders"
    login_api = CGdsConfig.server + "/dgs/api/ec/user/passwordlogin"
    create_order_api = CGdsConfig.server + "/dgs/api/ec/order/create"
    close_order_api = CGdsConfig.server + "/dgs/api/ec/order/updatestatus"

    dict_stats = {
        "parameters": {
            "running": running,
            "list_str_func": list_str_func,
            "list_func_weights": list_func_weights,
            "speed": speed,
            "noise": noise
        },
        "api": {
            "login_normal": "用户正常登录",
            "login_no_user": "用户登录失败，没有该用户",
            "login_passwd_error": "用户登录失败，密码错误",
            "create_order_amount": "创建订单失败，库存不足",
            "create_order_normal": "创建订单成功",
            "create_order_price": "创建订单失败，价格不正确",
            "query_order_normal": "查询订单成功",
            "query_order_timeout": "查询订单超时",
            "pay_order_cancel": "取消订单",
            "pay_order_normal": "订单支付成功"
        }
    }

    session = None

    @classmethod
    def main(cls, loop):
        asyncio.set_event_loop(loop)
        cls.session = aiohttp.ClientSession()
        loop.run_until_complete(cls.start())

    @classmethod
    async def start(cls):
        # 将 running 的状态置为 false 的时候，整个事件循环并没有停止
        while True:
            if cls.running:
                list_str_func = cls.list_str_func
                list_weights = cls.list_func_weights
                now = datetime.datetime.now()
                req_num = int(CGdsTs.calc_current(now, cls.noise) * cls.speed)
                list_func = random.choices(list_str_func, list_weights, k=req_num)

                if list_func:
                    task = []
                    for func in list_func:
                        task.append(asyncio.ensure_future(cls.reflect(func)))
                    await asyncio.wait(task)
                    logging.info("*" * 90 + " %s " % req_num + "*" * 90)
            await asyncio.sleep(1)

    @classmethod
    async def get_cookie(cls):
        res_login_normal = await cls.login_normal()
        cookie = "accountId=%s; token=%s" % (
            res_login_normal.get("data").get("accountId"), res_login_normal.get("data").get("token"))
        header = {
            "Cookie": cookie
        }
        return header

    @classmethod
    @CGdsWrapper.retry(desc=login_api)
    async def login_normal(cls):
        user = "test%s" % random.randint(1, 10000)
        payload = {
            "account": user,
            "password": 123456
        }
        return await CGdsAReq.AReq_post(cls.session, cls.login_api, data=payload)

    @classmethod
    async def login_no_user(cls):
        payload = {
            "account": "no_user",
            "password": 123456
        }
        return await CGdsAReq.AReq_post(cls.session, cls.login_api, data=payload)

    @classmethod
    async def login_passwd_error(cls):
        payload = {
            "account": "test1",
            "password": "error password"
        }
        return await CGdsAReq.AReq_post(cls.session, cls.login_api, data=payload)

    @classmethod
    @CGdsWrapper.retry(desc=create_order_api)
    async def create_order_normal(cls, header=None):
        # 登录
        if not header:
            header = await cls.get_cookie()

        payload = {
            "goodId": random.randint(1, 1000),
            "price": 88.88,
            "amount": 1,
            "payType": "alipay"
        }
        return await CGdsAReq.AReq_post(cls.session, cls.create_order_api, data=payload, header=header)

    @classmethod
    async def create_order_price(cls, header=None):
        # 登录
        if not header:
            header = await cls.get_cookie()

        payload = {
            "goodId": random.randint(1, 6900000),
            "price": 99.88,
            "amount": 1,
            "payType": "alipay"
        }
        return await CGdsAReq.AReq_post(cls.session, cls.create_order_api, data=payload, header=header)

    @classmethod
    async def create_order_amount(cls, header=None):
        # 登录
        if not header:
            header = await cls.get_cookie()

        payload = {
            "goodId": random.randint(1, 6900000),
            "price": 88.88,
            "amount": 10000,
            "payType": "alipay"
        }
        return await CGdsAReq.AReq_post(cls.session, cls.create_order_api, data=payload, header=header)

    @classmethod
    @CGdsWrapper.retry(desc=close_order_api)
    async def pay_order_normal(cls, header=None):
        # 登录
        if not header:
            header = await cls.get_cookie()

        # 创建订单
        res_create_order_normal = await cls.create_order_normal(header=header)
        orderId = res_create_order_normal.get("data").get("orderId")

        # 支付订单
        payload = {
            "orderId": orderId,
            "status": "done"
        }
        return await CGdsAReq.AReq_post(cls.session, cls.close_order_api, data=payload, header=header)

    @classmethod
    async def pay_order_cancel(cls, header=None):
        # 登录
        if not header:
            header = await cls.get_cookie()

        # 创建订单
        res_create_order_normal = await cls.create_order_normal(header=header)
        orderId = res_create_order_normal.get("data").get("orderId")

        # 取消订单
        payload = {
            "orderId": orderId,
            "status": "cancel"
        }
        return await CGdsAReq.AReq_post(cls.session, cls.close_order_api, data=payload, header=header)

    @classmethod
    async def query_order_timeout(cls, header=None):
        # 登录
        if not header:
            header = await cls.get_cookie()

        payload = {
            "page": 1,
            "size": 10000,
            "status": "all"
        }
        return await CGdsAReq.AReq_get(cls.session, cls.query_order_api, params=payload, header=header)

    @classmethod
    @CGdsWrapper.retry(desc=query_order_api)
    async def query_order_normal(cls, header=None):
        # 登录
        if not header:
            header = await cls.get_cookie()

        payload = {
            "page": 1,
            "size": 100,
            "status": "all"
        }
        return await CGdsAReq.AReq_get(cls.session, cls.query_order_api, params=payload, header=header)

    @classmethod
    async def reflect(cls, str_func):
        try:
            func = getattr(cls, str_func)
            res_data = await func()
            return res_data
        except AttributeError as e:
            logging.warning("no founded function %s" % e)
        except RuntimeError as e:
            pass


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    with futures.ThreadPoolExecutor(max_workers=4) as tp:
        tp.submit(CGdsEc.main, loop)
