import time

import requests

url = "http://127.0.0.1:5000/generate/config"
payload = {
}
response = requests.post(url=url, json=payload)
print(response.json())
print("-" * 160)

url = "http://127.0.0.1:5000/get/config"
response = requests.get(url=url)
print(response.json())
print("-" * 160)

url = "http://127.0.0.1:5000/generate/traces"
response = requests.post(url=url, json=payload)
print(response.json())
print("-" * 160)

url = "http://127.0.0.1:5000/get/traces"
response = requests.get(url=url)
print(response.json())
print("-" * 160)

url = "http://127.0.0.1:5000/get/speed"
response = requests.get(url=url)
print(response.json())
print("-" * 160)

url = "http://127.0.0.1:5000/stop"
payload = {
    "exp": "len(cls.traces)==10"
}
response = requests.post(url=url, json=payload)
print(response.json())
print("-" * 160)

url = "http://127.0.0.1:5000/update/traces/del"
payload = {}
response = requests.post(url=url, json=payload)
print(response.json())
print("-" * 160)

url = "http://127.0.0.1:5000/get/traces"
response = requests.get(url=url)
print(response.json())
print("-" * 160)

url = "http://127.0.0.1:5000/update/traces/add"
payload = {}
response = requests.post(url=url, json=payload)
print(response.json())
print("-" * 160)

url = "http://127.0.0.1:5000/get/traces"
response = requests.get(url=url)
print(response.json())
print("-" * 160)

url = "http://127.0.0.1:5000/start"
payload = {
    "speed": 100000
}
response = requests.post(url=url, json=payload)
print(response.json())
print("-" * 160)

# url = "http://127.0.0.1:5000/start"
# payload = {}
# response = requests.post(url=url, json=payload)
# print(response.json())
# print("-" * 160)

time.sleep(4)

url = "http://127.0.0.1:5000/get/speed"
response = requests.get(url=url)
print(response.json())
print("-" * 160)

time.sleep(4)
url = "http://127.0.0.1:5000/stop"
payload = {}
response = requests.post(url=url, json=payload)
print(response.json())
print("-" * 160)

# url = "http://127.0.0.1:5000/get/speed"
# response = requests.get(url=url)
# print(response.json())
# print("-" * 160)
