import time

import requests

cookies = {
    'UA': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkdXJhdGlvbiI6MzYwMDAwMDAwLCJsYXN0TG9naW4iOjE2MjU1MzgzOTM2NjIsIm5hbWVzIjoiW1wiamF4XCIsXCJ2aXNpb25cIixcImRhdGFNb2Rlcm5pemF0aW9uXCIsXCJkZWFsQW5hbHlzaXNcIixcImNtZGJcIixcImxvZ0FuYWx5c2lzXCIsXCJsb2dTcGVlZFwiLFwicmVmaW5lclwiXSIsInNpbmdsZVNpZ25PbiI6ZmFsc2UsInNlc3Npb25JZCI6IjM0ZTE5OGY3LTRjNGUtNDU0Mi05YmZhLWU0NTY3NDkzMzEwZiIsInVzZXJJZCI6ImVibWdyem1tRnV5WGl3RnRhVlJUcDhhVXdobDBGZnovVFJWNTBGWjRXR3VMSE8rdDRRd081VExMaDdDVTlWUU03STVEclQrb0JaWUdUN3JPN0N6NTVFT1dCcjZYQWZyL2ZiS3ZHYVdTMWlsbmp6RnBaT1J6VlBhL21LQzRBejlta2g0SGlVOXF3RnlNc3BURlB5VHk2dXNLTnUyU3c0L09hRWxRZ2J0M3c3dz0iLCJwcm9kdWN0cyI6IntcInJlZmluZXJcIjp7XCJTdG9ybVwiOlwiTi9BXCIsXCLpooTorabnrqHnkIZcIjpcIjEwMFwifX0ifQ.LxYxkWAZ02QR6eDqP0-Vy9fiBJjrHer9SC2P4Oh1P7z1KkZCtIvnvFwhGIN6CtATZLT8oVuCTWnqNOVyddNxGA',
}

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'DNT': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'http://192.168.31.92:8080',
    'Referer': 'http://192.168.31.92:8080/dealAnalysis/deal/model/model',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6',
}
for i in range(3, 40):
    data = '{"modelId":null,"modelParameter":{"time_field":null,"count_field":null,"latency_field":null,"rate_field":null,"window":120,"count_increase_sigma":1,"count_drop_sigma":1,"count_upper_constant":-1,"count_lower_constant":-1,"count_detect_mode":"both-both","latency_increase_sigma":1,"latency_drop_sigma":1,"latency_upper_constant":-1,"latency_lower_constant":-1,"latency_detect_mode":"both-increase","rate_increase_sigma":1,"rate_drop_sigma":1,"rate_upper_constant":100,"rate_lower_constant":0,"rate_detect_mode":"both-drop","latency_weight":0.2},"modelDescription":"","modelName":"mad_%s","modelSource":"manual","aggFunc":"count","aggWindow":1,"aggUnit":"minute","algClass":"python.flink.mad.Mad.MAD","modelData":null,"algTrainDataLength":null,"algName":"Mad","algAlias":"Mad","algVersion":"1.0.0","algDescription":null,"algDetectType":"0","algProcessType":"0","algDataType":"0","algTrainJob":"","algTrainType":"0","algParameters":[{"name":"time_field","label":"\u65F6\u95F4\u5B57\u6BB5\u540D","type":["STRING"],"description":"\u6307\u5B9A\u65F6\u95F4\u5B57\u6BB5\u540D","optional":false,"defaultValue":null,"algParameterType":"STATIC"},{"name":"count_field","label":"\u6570\u91CF\u7C7B\u6307\u6807\u5B57\u6BB5\u540D","type":["STRING"],"description":"\u6307\u5B9A\u6570\u91CF\u7C7B\u6307\u6807\u5B57\u6BB5\u540D,\u53EF\u6307\u5B9A\u4E00\u4E2A\u6216\u591A\u4E2A\u5B57\u6BB5,\u7528\u5206\u53F7\u5206\u9694","optional":false,"defaultValue":null,"algParameterType":"STATIC"},{"name":"latency_field","label":"\u5EF6\u65F6\u7C7B\u6307\u6807\u5B57\u6BB5\u540D","type":["STRING"],"description":"\u6307\u5B9A\u5EF6\u65F6\u7C7B\u6307\u6807\u5B57\u6BB5\u540D,\u53EF\u6307\u5B9A\u4E00\u4E2A\u6216\u591A\u4E2A\u5B57\u6BB5,\u7528\u5206\u53F7\u5206\u9694","optional":false,"defaultValue":null,"algParameterType":"STATIC"},{"name":"rate_field","label":"\u6210\u529F\u7387\u7C7B\u6307\u6807\u5B57\u6BB5\u540D","type":["STRING"],"description":"\u6307\u5B9A\u6210\u529F\u7387\u7C7B\u6307\u6807\u5B57\u6BB5\u540D,\u53EF\u6307\u5B9A\u4E00\u4E2A\u6216\u591A\u4E2A\u5B57\u6BB5,\u7528\u5206\u53F7\u5206\u9694","optional":false,"defaultValue":null,"algParameterType":"STATIC"},{"name":"window","label":"\u7EDF\u8BA1\u7A97\u53E3","type":["INT"],"description":"\u5386\u53F2\u6570\u636E\u5F71\u54CD\u8303\u56F4","optional":true,"defaultValue":"120","algParameterType":"STATIC"},{"name":"count_increase_sigma","label":"\u6570\u91CF\u7C7B\u6307\u6807\u7A81\u589E\u654F\u611F\u5EA6","type":["FLOAT"],"description":"\u8C03\u8282\u6570\u91CF\u7C7B\u6307\u6807\u4E0A\u754C\u8303\u56F4","optional":true,"defaultValue":"1.0","algParameterType":"STATIC"},{"name":"count_drop_sigma","label":"\u6570\u91CF\u7C7B\u6307\u6807\u7A81\u964D\u654F\u611F\u5EA6","type":["FLOAT"],"description":"\u8C03\u8282\u6570\u91CF\u7C7B\u6307\u6807\u4E0B\u754C\u8303\u56F4","optional":true,"defaultValue":"1.0","algParameterType":"STATIC"},{"name":"count_upper_constant","label":"\u6570\u91CF\u7C7B\u6307\u6807\u4E0A\u754C\u9608\u503C","type":["FLOAT"],"description":"\u6570\u91CF\u7C7B\u6307\u6807\u4E0A\u754C\u9608\u503C\uFF0C\u9ED8\u8BA4-1.0\uFF0C\u8868\u793A\u4E0D\u8FDB\u884C\u9650\u5B9A\uFF0C\u6309\u5B9E\u9645\u4E1A\u52A1\u6570\u636E\u8C03\u6574\u3002","optional":true,"defaultValue":"-1.0","algParameterType":"STATIC"},{"name":"count_lower_constant","label":"\u6570\u91CF\u7C7B\u6307\u6807\u4E0B\u754C\u9608\u503C","type":["FLOAT"],"description":"\u6570\u91CF\u7C7B\u6307\u6807\u4E0B\u754C\u9608\u503C\uFF0C\u9ED8\u8BA4-1.0\uFF0C\u8868\u793A\u4E0D\u8FDB\u884C\u9650\u5B9A\uFF0C\u6309\u5B9E\u9645\u4E1A\u52A1\u6570\u636E\u8C03\u6574\u3002","optional":true,"defaultValue":"-1.0","algParameterType":"STATIC"},{"name":"count_detect_mode","label":"\u6570\u91CF\u7C7B\u6307\u6807\u68C0\u6D4B\u6A21\u5F0F","type":["STRING"],"description":"\u6570\u91CF\u7C7B\u6307\u6807\u68C0\u6D4B\u6A21\u5F0F\uFF0C\u53EF\u9009both-both\u3001soft-both\u3001hard-both\u3001both-increase\u3001both-drop\u3001soft-increase\u3001soft-drop\u3001hard-increase\u3001hard-drop","optional":true,"defaultValue":"both-both","algParameterType":"STATIC"},{"name":"latency_increase_sigma","label":"\u5EF6\u65F6\u7C7B\u6307\u6807\u7A81\u589E\u654F\u611F\u5EA6","type":["FLOAT"],"description":"\u8C03\u8282\u5EF6\u65F6\u7C7B\u6307\u6807\u4E0A\u754C\u8303\u56F4","optional":true,"defaultValue":"1.0","algParameterType":"STATIC"},{"name":"latency_drop_sigma","label":"\u5EF6\u65F6\u7C7B\u6307\u6807\u7A81\u964D\u654F\u611F\u5EA6","type":["FLOAT"],"description":"\u8C03\u8282\u5EF6\u65F6\u7C7B\u6307\u6807\u4E0B\u754C\u8303\u56F4","optional":true,"defaultValue":"1.0","algParameterType":"STATIC"},{"name":"latency_upper_constant","label":"\u5EF6\u65F6\u7C7B\u6307\u6807\u4E0A\u754C\u9608\u503C","type":["FLOAT"],"description":"\u5EF6\u65F6\u7C7B\u6307\u6807\u4E0A\u754C\u9608\u503C\uFF0C\u9ED8\u8BA4-1.0\uFF0C\u8868\u793A\u4E0D\u8FDB\u884C\u9650\u5B9A\uFF0C\u6309\u5B9E\u9645\u4E1A\u52A1\u6570\u636E\u8C03\u6574\u3002","optional":true,"defaultValue":"-1.0","algParameterType":"STATIC"},{"name":"latency_lower_constant","label":"\u5EF6\u65F6\u7C7B\u6307\u6807\u4E0B\u754C\u9608\u503C","type":["FLOAT"],"description":"\u5EF6\u65F6\u7C7B\u6307\u6807\u4E0B\u754C\u9608\u503C\uFF0C\u9ED8\u8BA4-1.0\uFF0C\u8868\u793A\u4E0D\u8FDB\u884C\u9650\u5B9A\uFF0C\u6309\u5B9E\u9645\u4E1A\u52A1\u6570\u636E\u8C03\u6574\u3002","optional":true,"defaultValue":"-1.0","algParameterType":"STATIC"},{"name":"latency_detect_mode","label":"\u5EF6\u65F6\u7C7B\u6307\u6807\u68C0\u6D4B\u6A21\u5F0F","type":["STRING"],"description":"\u5EF6\u65F6\u7C7B\u6307\u6807\u68C0\u6D4B\u6A21\u5F0F\uFF0C\u53EF\u9009both-both\u3001soft-both\u3001hard-both\u3001both-increase\u3001both-drop\u3001soft-increase\u3001soft-drop\u3001hard-increase\u3001hard-drop","optional":true,"defaultValue":"both-increase","algParameterType":"STATIC"},{"name":"rate_increase_sigma","label":"\u6210\u529F\u7387\u7C7B\u6307\u6807\u7A81\u589E\u654F\u611F\u5EA6","type":["FLOAT"],"description":"\u8C03\u8282\u6210\u529F\u7387\u7C7B\u6307\u6807\u4E0A\u754C\u8303\u56F4","optional":true,"defaultValue":"1.0","algParameterType":"STATIC"},{"name":"rate_drop_sigma","label":"\u6210\u529F\u7387\u7C7B\u6307\u6807\u7A81\u964D\u654F\u611F\u5EA6","type":["FLOAT"],"description":"\u8C03\u8282\u6210\u529F\u7387\u7C7B\u6307\u6807\u4E0B\u754C\u8303\u56F4","optional":true,"defaultValue":"1.0","algParameterType":"STATIC"},{"name":"rate_upper_constant","label":"\u6210\u529F\u7387\u7C7B\u6307\u6807\u4E0A\u754C\u9608\u503C","type":["FLOAT"],"description":"\u6210\u529F\u7387\u7C7B\u6307\u6807\u4E0A\u754C\u9608\u503C\uFF0C\u9ED8\u8BA4-1.0\uFF0C\u8868\u793A\u4E0D\u8FDB\u884C\u9650\u5B9A\uFF0C\u6309\u5B9E\u9645\u4E1A\u52A1\u6570\u636E\u8C03\u6574\u3002","optional":true,"defaultValue":"100.0","algParameterType":"STATIC"},{"name":"rate_lower_constant","label":"\u6210\u529F\u7387\u7C7B\u6307\u6807\u4E0B\u754C\u9608\u503C","type":["FLOAT"],"description":"\u6210\u529F\u7387\u7C7B\u6307\u6807\u4E0B\u754C\u9608\u503C\uFF0C\u9ED8\u8BA4-1.0\uFF0C\u8868\u793A\u4E0D\u8FDB\u884C\u9650\u5B9A\uFF0C\u6309\u5B9E\u9645\u4E1A\u52A1\u6570\u636E\u8C03\u6574\u3002","optional":true,"defaultValue":"0.0","algParameterType":"STATIC"},{"name":"rate_detect_mode","label":"\u6210\u529F\u7387\u7C7B\u6307\u6807\u68C0\u6D4B\u6A21\u5F0F","type":["STRING"],"description":"\u6210\u529F\u7387\u7C7B\u6307\u6807\u68C0\u6D4B\u6A21\u5F0F\uFF0C\u53EF\u9009both-both\u3001soft-both\u3001hard-both\u3001both-increase\u3001both-drop\u3001soft-increase\u3001soft-drop\u3001hard-increase\u3001hard-drop","optional":true,"defaultValue":"both-drop","algParameterType":"STATIC"},{"name":"latency_weight","label":"\u5EF6\u65F6\u6743\u91CD","type":["FLOAT"],"description":"\u5065\u5EB7\u5EA6\u5EF6\u65F6\u6307\u6807\u6240\u5360\u6743\u91CD","optional":true,"defaultValue":"0.2","algParameterType":"STATIC"}]}' % i

    response = requests.post('http://192.168.31.92:8080/dealAnalysis/api/model', headers=headers, cookies=cookies,
                             data=data.encode("utf-8"), verify=False)

    print(response.text)

    time.sleep(0.4)