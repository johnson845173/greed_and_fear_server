import requests

data = requests.get("http://api.greedandfear.fun/api/tc/")
# data = requests.get("http://127.0.0.1:8000/api/tc/")

print(data.headers)