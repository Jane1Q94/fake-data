import time
import random

import requests

cookies = {
    'UA': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkdXJhdGlvbiI6MzYwMDAwMDAwLCJsYXN0TG9naW4iOjE2MjUxMDg5NDIwMDcsIm5hbWVzIjoiW1wiamF4XCIsXCJ2aXNpb25cIixcImRhdGFNb2Rlcm5pemF0aW9uXCIsXCJkZWFsQW5hbHlzaXNcIixcImNtZGJcIixcImxvZ0FuYWx5c2lzXCIsXCJsb2dTcGVlZFwiLFwicmVmaW5lclwiXSIsInNpbmdsZVNpZ25PbiI6ZmFsc2UsInNlc3Npb25JZCI6IjQzODBmYmFhLWViOTgtNDUyMS1iYjRjLTRhZThmNWIwZTNmYSIsInVzZXJJZCI6ImVibWdyem1tRnV5WGl3RnRhVlJUcDhhVXdobDBGZnovVFJWNTBGWjRXR3VMSE8rdDRRd081VExMaDdDVTlWUU03STVEclQrb0JaWUdUN3JPN0N6NTVFT1dCcjZYQWZyL2ZiS3ZHYVdTMWlsbmp6RnBaT1J6VlBhL21LQzRBejlta2g0SGlVOXF3RnlNc3BURlB5VHk2dXNLTnUyU3c0L09hRWxRZ2J0M3c3dz0iLCJwcm9kdWN0cyI6IntcInJlZmluZXJcIjp7XCJTdG9ybVwiOlwiTi9BXCIsXCLpooTorabnrqHnkIZcIjpcIjEwMFwifX0ifQ.QVftoSGbh7NKmyrxTLdNFoh9WOSOnwBnBWBAntHaFAyVSBk221riCH4rOrAKwrR0PakD0yfEX4pexFQ63m7tZw',
}

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'DNT': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'http://192.168.31.92:8080',
    'Referer': 'http://192.168.31.92:8080/dealAnalysis/metric/call-chain/view/0',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6',
}

for i in range(200,220):
    granularity = random.choice([1, 5, 10])
    data = '{"id":null,"name":"test_%s","dsId":2492733820732416,"dsName":"skywalking_10","granularity":%s,"servingSort":"warnCount","healthEnable":1,"healthRule":"[{\\"logic\\":\\"\\",\\"key\\":\\"alertCount\\",\\"label\\":\\"\u544A\u8B66\u603B\u6570\\",\\"value\\":{\\"health\\":[0,1],\\"notice\\":[1,2],\\"danger\\":[2,null]}}]","startServings":[{"instanceId":2492733980705804,"instanceName":"matrix rich synergies"}],"attentionServings":[{"instanceId":2492733980476454,"instanceName":"syndicate integrated e-markets"}]}' % (i, granularity)
    response = requests.post('http://192.168.31.92:8080/dealAnalysis/api/call-chain/view', headers=headers, cookies=cookies, data=data.encode("utf-8"), verify=False)
    print(response.text)
    time.sleep(0.01)
