import requests

host = "https://api.greedandfear.fun"
host = "http://127.0.0.1:8000"

response = requests.post(url=f"{host}/api/login/",json={"phone_number":7899404714,"password":"12345678"})

# print(response.json())
print(response.content)
print(response.headers)
print(response.status_code)