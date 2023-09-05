import requests
import redis
import time


def set_redis_otp(phone_number,otp,validity=60):

    r = redis.Redis(host='cache.greedandfear.fun', port=6379, decode_responses=True,password="eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81")

    r.set(name=phone_number,value=otp,ex=validity)

    r.close()

def get_redis_otp(phone_numbery):
    r = redis.Redis(host='cache.greedandfear.fun', port=6379, decode_responses=True,password="eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81")

    stored_otp = r.get(name=phone_numbery)
    
    r.close()

    return stored_otp

def clear_redis():
    r = redis.Redis(host='cache.greedandfear.fun', port=6379, decode_responses=True,password="eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81")

    keys = r.keys('*')
    r.delete(*keys)

    r.close()

# clear_redis()
# phone_number = "917899404714"

# set_redis_otp(phone_number=phone_number,otp=123456789)
# print(get_redis_otp(phone_numbery=phone_number))

