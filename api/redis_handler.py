import requests
import redis

r = redis.Redis(host='cache.greedandfear.fun', port=6379, decode_responses=True,password="eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81")


for i in range(10):
    r.set(i,i)