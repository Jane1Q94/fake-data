import time

import requests

serverInsNum = 10
serverEndPointNum = 10

# url = "http://192.168.102.10:5001/generate/config"
# payload = {
#     "serverNum": 100
# }
# response = requests.post(url=url, json=payload)
# print(response.json())
# print("-" * 160)
#
# url = "http://192.168.102.10:5001/generate/traces"
# payload = {
#     "traceNum": 10
# }
# response = requests.post(url=url, json=payload)
# print(response.json())
# print("-" * 160)
#
# url = "http://192.168.102.10:5001/get/config"
# response = requests.get(url=url)
# print(response.json())
# print("-" * 160)

url = "http://192.168.102.10:5001/get/traces"
response = requests.get(url=url)
print(response.json())
print("-" * 160)

# url = "http://192.168.102.10:5001/start"
# payload = {}
# response = requests.post(url=url, json=payload)
# print(response.json())
# print("-" * 160)
#
# url = "http://192.168.102.10:5001/output"
# payload = {
#     "address": "192.168.101.11:9092",
#     "topic": "skywalking-11"
# }
# response = requests.post(url=url, json=payload)
# print(response.json())
# print("-" * 160)


endpoint = 'engineer innovative networks@122.192.225.85@explore/explore/tag/tag'
# endpoint = "unleash dot-com niches@181.133.137.252@blog/search/categories/explore"
url = "http://192.168.102.10:5001/update/delay"
payload = {
    "endpoint": endpoint,
    "delay": [1000, 1500]
}
response = requests.post(url=url, json=payload)
print(response.json())
print("-" * 160)


