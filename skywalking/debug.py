import requests

url = "http://127.0.0.1:5000/start"
payload = {
    "serverNum": 10,
    "serverInsNum": 10,
    "serverEndPointNum": 10,
    "traceNum": 4
}
response = requests.post(url=url, json=payload)
if response.status_code == 200:
    print(response.json())
else:
    print("错误")
