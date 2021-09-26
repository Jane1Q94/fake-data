import aiohttp
from GdsWrapper import CGdsWrapper


class CGdsAReq:
    # 并发数
    SESSION = aiohttp.ClientSession()

    @classmethod
    @CGdsWrapper.record_time
    async def AReq_post(cls, session, url, data, header=None):
        async with session.post(url, json=data, timeout=100, headers=header) as res:
            # logging.info("request to %s" % url)
            res_data = await res.json(encoding="utf-8")
            return res_data, url, data, header

    @classmethod
    @CGdsWrapper.record_time
    async def AReq_get(cls, url, params, header=None):
        async with cls.SESSION.get(url, params=params, timeout=100, headers=header) as res:
            # logging.info("request to %s" % url)
            res_data = await res.json(encoding="utf-8")
            return res_data, url, params, header

    @classmethod
    @CGdsWrapper.record_time
    async def AReq_put(cls, url, data, header=None):
        async with cls.SESSION.put(url, json=data, timeout=100, headers=header) as res:
            # logging.info("request to %s" % url)
            res_data = await res.json(encoding="utf-8")
            return res_data, url, data, header

    @classmethod
    async def AReq_post_data(cls, url, data, header=None):
        session = aiohttp.ClientSession()
        if not header:
            header = {'Content-Type': 'application/json'}
        async with session.post(url, data=data, timeout=100, headers=header) as res:
            res_data = await res.json(encoding="utf-8")
            return res_data
