import http.client

conn = http.client.HTTPSConnection("apigway-uat.canarabank.in")

payload = "{\"Request\":{\"body\":{\"encryptData\":{\"accountNumber\":\"01222200125833\",\"startDate\":\"15/05/2023\",\"endDate\":\"30/05/2023\",\"uniqueRefNo\":\"NEFT12345\"}}}}"

headers = {
    'X-IBM-Client-Id': "fb2432f27714891dc936e7d320b99193",
    'X-IBM-Client-Secret': "0356ab8404552ab3a33537a1ac525b7e",
    'content-type': "application/json",
    'accept': "application/json"
    }

conn.request("POST", "/sandbox/s-dab/apib/inwardNeft/statement", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))