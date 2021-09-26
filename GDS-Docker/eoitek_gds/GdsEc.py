import asyncio
import datetime
import random
import aiohttp
from eoitek_gds import logging
from GdsTs import CGdsTs
from GdsAReq import CGdsAReq
from concurrent import futures
import faker

fk = faker.Faker()


class CGdsEc:
    dict_api = {
        "success": True,
        "code": "20000",
        "message": "",
        "data": {
            "login_normal": {
                "name": "用户正常登录",
                "author": "YangJiJian",
                "status": "running",
                "api": "http://192.168.101.11:8787/dgs/api/ec/user/passwordlogin",
                "speed": 10,
                "noise": 0.2,
                "user-agent": [fk.user_agent() for _ in range(10)],
                "user-agent-weights": [1 for _ in range(10)],
                "ip": [fk.ipv4_public() for _ in range(10)],
                "ip-weights": [1 for _ in range(10)],
                "refer": ["http://www.google.com", "http://www.baidu.com", "http://www.bing.com",
                          "http://www.sougou.com", "http://www.weixin.com",
                          "http://www.eoitek.net"],
                "refer-weights": [1 for _ in range(6)],
            },
            "login_no_user": {
                "name": "用户登录失败，没有该用户",
                "author": "YangJiJian",
                "status": "running",
                "api": "http://192.168.101.11:8787/dgs/api/ec/user/passwordlogin",
                "speed": 10,
                "noise": 0.2,
                "user-agent": [fk.user_agent() for _ in range(10)],
                "user-agent-weights": [1 for _ in range(10)],
                "ip": [fk.ipv4_public() for _ in range(10)],
                "ip-weights": [1 for _ in range(10)],
                "refer": ["http://www.google.com", "http://www.baidu.com", "http://www.bing.com",
                          "http://www.sougou.com", "http://www.weixin.com",
                          "http://www.eoitek.net"],
                "refer-weights": [1 for _ in range(6)],
            },
            "login_passwd_error": {
                "name": "用户登录失败，密码错误",
                "author": "YangJiJian",
                "status": "running",
                "api": "http://192.168.101.11:8787/dgs/api/ec/user/passwordlogin",
                "speed": 10,
                "noise": 0.2,
                "user-agent": [fk.user_agent() for _ in range(10)],
                "user-agent-weights": [1 for _ in range(10)],
                "ip": [fk.ipv4_public() for _ in range(10)],
                "ip-weights": [1 for _ in range(10)],
                "refer": ["http://www.google.com", "http://www.baidu.com", "http://www.bing.com",
                          "http://www.sougou.com", "http://www.weixin.com",
                          "http://www.eoitek.net"],
                "refer-weights": [1 for _ in range(6)],

            },
            "create_order_amount": {
                "name": "创建订单失败，库存不足",
                "author": "YangJiJian",
                "status": "running",
                "api": "http://192.168.101.11:8787/dgs/api/ec/order/create",
                "speed": 10,
                "noise": 0.2,
                "user-agent": [fk.user_agent() for _ in range(10)],
                "user-agent-weights": [1 for _ in range(10)],
                "ip": [fk.ipv4_public() for _ in range(10)],
                "ip-weights": [1 for _ in range(10)],
                "refer": ["http://www.google.com", "http://www.baidu.com", "http://www.bing.com",
                          "http://www.sougou.com", "http://www.weixin.com",
                          "http://www.eoitek.net"],
                "refer-weights": [1 for _ in range(6)],
            },
            "create_order_normal": {
                "name": "创建订单成功",
                "author": "YangJiJian",
                "status": "running",
                "api": "http://192.168.101.11:8787/dgs/api/ec/order/create",
                "speed": 10,
                "noise": 0.2,
                "user-agent": [fk.user_agent() for _ in range(10)],
                "user-agent-weights": [1 for _ in range(10)],
                "ip": [fk.ipv4_public() for _ in range(10)],
                "ip-weights": [1 for _ in range(10)],
                "refer": ["http://www.google.com", "http://www.baidu.com", "http://www.bing.com",
                          "http://www.sougou.com", "http://www.weixin.com",
                          "http://www.eoitek.net"],
                "refer-weights": [1 for _ in range(6)],
            },
            "create_order_price": {
                "name": "创建订单失败，价格不正确",
                "author": "YangJiJian",
                "status": "running",
                "api": "http://192.168.101.11:8787/dgs/api/ec/order/create",
                "speed": 10,
                "noise": 0.2,
                "user-agent": [fk.user_agent() for _ in range(10)],
                "user-agent-weights": [1 for _ in range(10)],
                "ip": [fk.ipv4_public() for _ in range(10)],
                "ip-weights": [1 for _ in range(10)],
                "refer": ["http://www.google.com", "http://www.baidu.com", "http://www.bing.com",
                          "http://www.sougou.com", "http://www.weixin.com",
                          "http://www.eoitek.net"],
                "refer-weights": [1 for _ in range(6)],
            },
            "query_order_normal": {
                "name": "查询订单成功",
                "author": "YangJiJian",
                "status": "running",
                "api": "http://192.168.101.11:8787/dgs/api/ec/orders",
                "speed": 10,
                "noise": 0.2,
                "user-agent": [fk.user_agent() for _ in range(10)],
                "user-agent-weights": [1 for _ in range(10)],
                "ip": [fk.ipv4_public() for _ in range(10)],
                "ip-weights": [1 for _ in range(10)],
                "refer": ["http://www.google.com", "http://www.baidu.com", "http://www.bing.com",
                          "http://www.sougou.com", "http://www.weixin.com",
                          "http://www.eoitek.net"],
                "refer-weights": [1 for _ in range(6)],

            },
            "query_order_timeout": {
                "name": "查询订单超时",
                "author": "YangJiJian",
                "status": "running",
                "api": "http://192.168.101.11:8787/dgs/api/ec/orders",
                "speed": 10,
                "noise": 0.2,
                "user-agent": [fk.user_agent() for _ in range(10)],
                "user-agent-weights": [1 for _ in range(10)],
                "ip": [fk.ipv4_public() for _ in range(10)],
                "ip-weights": [1 for _ in range(10)],
                "refer": ["http://www.google.com", "http://www.baidu.com", "http://www.bing.com",
                          "http://www.sougou.com", "http://www.weixin.com",
                          "http://www.eoitek.net"],
                "refer-weights": [1 for _ in range(6)],
            },
            "pay_order_cancel": {
                "name": "取消订单",
                "author": "YangJiJian",
                "status": "running",
                "api": "http://192.168.101.11:8787/dgs/api/ec/order/updatestatus",
                "speed": 10,
                "noise": 0.2,
                "user-agent": [fk.user_agent() for _ in range(10)],
                "user-agent-weights": [1 for _ in range(10)],
                "ip": [fk.ipv4_public() for _ in range(10)],
                "ip-weights": [1 for _ in range(10)],
                "refer": ["http://www.google.com", "http://www.baidu.com", "http://www.bing.com",
                          "http://www.sougou.com", "http://www.weixin.com",
                          "http://www.eoitek.net"],
                "refer-weights": [1 for _ in range(6)],
            },
            "pay_order_normal": {
                "name": "订单支付成功",
                "author": "YangJiJian",
                "status": "running",
                "api": "http://192.168.101.11:8787/dgs/api/ec/order/updatestatus",
                "speed": 10,
                "noise": 0.2,
                "user-agent": [fk.user_agent() for _ in range(10)],
                "user-agent-weights": [1 for _ in range(10)],
                "ip": [fk.ipv4_public() for _ in range(10)],
                "ip-weights": [1 for _ in range(10)],
                "refer": ["http://www.google.com", "http://www.baidu.com", "http://www.bing.com",
                          "http://www.sougou.com", "http://www.weixin.com",
                          "http://www.eoitek.net"],
                "refer-weights": [1 for _ in range(6)],
            }
        }
    }

    @classmethod
    def main(cls, loop, func_name):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(cls.start(func_name))

    @classmethod
    async def start(cls, func_name):
        # 将 running 的状态置为 false 的时候，整个事件循环并没有停止
        session = aiohttp.ClientSession()
        dict_parameters = cls.dict_api.get('data').get(func_name)
        while True:
            status = dict_parameters.get("status")
            noise = dict_parameters.get("noise")
            speed = dict_parameters.get("speed")
            if status == "running":
                now = datetime.datetime.now()
                req_num = int(CGdsTs.calc_current(now, noise) * speed)
                task = []
                for _ in range(req_num):
                    task.append(asyncio.ensure_future(cls.reflect(session, func_name)))
                await asyncio.wait(task)
                logging.info("*" * 40 + " 【%s】%s " % (func_name, req_num) + "*" * 40)
            await asyncio.sleep(1)

    @classmethod
    async def get_cookie(cls, session):
        list_user_agent = cls.dict_api.get("data").get("login_normal").get("user-agent")
        list_user_agent_weights = cls.dict_api.get("data").get("login_normal").get("user-agent-weights")
        list_ip = cls.dict_api.get("data").get("login_normal").get("ip")
        list_ip_weights = cls.dict_api.get("data").get("login_normal").get("ip-weights")
        list_refer = cls.dict_api.get("data").get("login_normal").get("refer")
        list_refer_weights = cls.dict_api.get("data").get("login_normal").get("refer-weights")

        header = {
            "user-agent": random.choices(list_user_agent, list_user_agent_weights)[0],
            "ip": random.choices(list_ip, list_ip_weights)[0],
            "refer": random.choices(list_refer, list_refer_weights)[0]
        }

        res_login_normal = await cls.login_normal(session, header=header)
        cookie = "accountId=%s; token=%s" % (
            res_login_normal.get("data").get("accountId"), res_login_normal.get("data").get("token"))

        header = {
            "Cookie": cookie,
            "user-agent": random.choices(list_user_agent, list_user_agent_weights)[0],
            "ip": random.choices(list_ip, list_ip_weights)[0],
            "refer": random.choices(list_refer, list_refer_weights)[0]
        }
        return header

    @classmethod
    async def login_normal(cls, session, header=None):
        api = cls.dict_api.get('data').get("login_normal").get("api")
        user = "test%s" % random.randint(1, 10000)
        payload = {
            "account": user,
            "password": 123456
        }
        if not header:
            list_user_agent = cls.dict_api.get("data").get("login_normal").get("user-agent")
            list_user_agent_weights = cls.dict_api.get("data").get("login_normal").get("user-agent-weights")
            list_ip = cls.dict_api.get("data").get("login_normal").get("ip")
            list_ip_weights = cls.dict_api.get("data").get("login_normal").get("ip-weights")
            list_refer = cls.dict_api.get("data").get("login_normal").get("refer")
            list_refer_weights = cls.dict_api.get("data").get("login_normal").get("refer-weights")
            header = {
                "user-agent": random.choices(list_user_agent, list_user_agent_weights)[0],
                "ip": random.choices(list_ip, list_ip_weights)[0],
                "refer": random.choices(list_refer, list_refer_weights)[0]
            }
        return await CGdsAReq.AReq_post(session, api, data=payload, header=header)

    @classmethod
    async def login_no_user(cls, session, header=None):
        api = cls.dict_api.get('data').get("login_no_user").get("api")
        payload = {
            "account": "no_user",
            "password": 123456
        }
        if not header:
            list_user_agent = cls.dict_api.get("data").get("login_normal").get("user-agent")
            list_user_agent_weights = cls.dict_api.get("data").get("login_normal").get("user-agent-weights")
            list_ip = cls.dict_api.get("data").get("login_normal").get("ip")
            list_ip_weights = cls.dict_api.get("data").get("login_normal").get("ip-weights")
            list_refer = cls.dict_api.get("data").get("login_normal").get("refer")
            list_refer_weights = cls.dict_api.get("data").get("login_normal").get("refer-weights")
            header = {
                "user-agent": random.choices(list_user_agent, list_user_agent_weights)[0],
                "ip": random.choices(list_ip, list_ip_weights)[0],
                "refer": random.choices(list_refer, list_refer_weights)[0]
            }
        return await CGdsAReq.AReq_post(session, api, data=payload, header=header)

    @classmethod
    async def login_passwd_error(cls, session, header=None):
        api = cls.dict_api.get('data').get("login_passwd_error").get("api")
        user = "test%s" % random.randint(1, 10000)
        payload = {
            "account": user,
            "password": "error password"
        }
        if not header:
            list_user_agent = cls.dict_api.get("data").get("login_normal").get("user-agent")
            list_user_agent_weights = cls.dict_api.get("data").get("login_normal").get("user-agent-weights")
            list_ip = cls.dict_api.get("data").get("login_normal").get("ip")
            list_ip_weights = cls.dict_api.get("data").get("login_normal").get("ip-weights")
            list_refer = cls.dict_api.get("data").get("login_normal").get("refer")
            list_refer_weights = cls.dict_api.get("data").get("login_normal").get("refer-weights")
            header = {
                "user-agent": random.choices(list_user_agent, list_user_agent_weights)[0],
                "ip": random.choices(list_ip, list_ip_weights)[0],
                "refer": random.choices(list_refer, list_refer_weights)[0]
            }
        return await CGdsAReq.AReq_post(session, api, data=payload, header=header)

    @classmethod
    async def create_order_normal(cls, session, header=None):
        api = cls.dict_api.get('data').get("create_order_normal").get("api")
        # 登录
        if not header:
            header = await cls.get_cookie(session)

        payload = {
            "goodId": random.randint(1, 1000),
            "price": 88.88,
            "amount": 1,
            "payType": "alipay"
        }
        return await CGdsAReq.AReq_post(session, api, data=payload, header=header)

    @classmethod
    async def create_order_price(cls, session, header=None):
        api = cls.dict_api.get('data').get("create_order_price").get("api")
        # 登录
        if not header:
            header = await cls.get_cookie(session)

        payload = {
            "goodId": random.randint(1, 6900000),
            "price": 99.88,
            "amount": 1,
            "payType": "alipay"
        }
        return await CGdsAReq.AReq_post(session, api, data=payload, header=header)

    @classmethod
    async def create_order_amount(cls, session, header=None):
        api = cls.dict_api.get('data').get("create_order_amount").get("api")
        # 登录
        if not header:
            header = await cls.get_cookie(session)

        payload = {
            "goodId": random.randint(1, 6900000),
            "price": 88.88,
            "amount": 10000,
            "payType": "alipay"
        }
        return await CGdsAReq.AReq_post(session, api, data=payload, header=header)

    @classmethod
    async def pay_order_normal(cls, session, header=None):
        api = cls.dict_api.get('data').get("pay_order_normal").get("api")
        # 登录
        if not header:
            header = await cls.get_cookie(session)

        # 创建订单
        res_create_order_normal = await cls.create_order_normal(session, header=header)
        orderId = res_create_order_normal.get("data").get("orderId")

        # 支付订单
        payload = {
            "orderId": orderId,
            "status": "done"
        }
        return await CGdsAReq.AReq_post(session, api, data=payload, header=header)

    @classmethod
    async def pay_order_cancel(cls, session, header=None):
        api = cls.dict_api.get('data').get("pay_order_cancel").get("api")
        # 登录
        if not header:
            header = await cls.get_cookie(session)

        # 创建订单
        res_create_order_normal = await cls.create_order_normal(session, header=header)
        orderId = res_create_order_normal.get("data").get("orderId")

        # 取消订单
        payload = {
            "orderId": orderId,
            "status": "cancel"
        }
        return await CGdsAReq.AReq_post(session, api, data=payload, header=header)

    @classmethod
    async def query_order_timeout(cls, session, header=None):
        api = cls.dict_api.get('data').get("query_order_timeout").get("api")
        # 登录
        if not header:
            header = await cls.get_cookie(session)

        payload = {
            "page": 1,
            "size": 10000,
            "status": "all"
        }
        return await CGdsAReq.AReq_get(session, api, params=payload, header=header)

    @classmethod
    async def query_order_normal(cls, session, header=None):
        api = cls.dict_api.get('data').get("query_order_normal").get("api")
        # 登录
        if not header:
            header = await cls.get_cookie(session)

        payload = {
            "page": 1,
            "size": 100,
            "status": "all"
        }
        return await CGdsAReq.AReq_get(session, api, params=payload, header=header)

    @classmethod
    async def reflect(cls, session, str_func):
        try:
            func = getattr(cls, str_func)
            res_data = await func(session)
            return res_data
        except AttributeError as e:
            logging.warning("no founded function %s" % e)
        except RuntimeError as e:
            pass


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    with futures.ThreadPoolExecutor(max_workers=4) as tp:
        tp.submit(CGdsEc.main, loop)
