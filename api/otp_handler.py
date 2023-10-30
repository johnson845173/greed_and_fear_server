try:
    from . import redis_handler
except:
    import redis_handler

import random

def preprocess_phone_number(phone_number):

    phone_number = str(phone_number)

    
    if phone_number.startswith('+'):
        phone_number = phone_number
    elif phone_number.startswith('0'):
        phone_number = '+91' + phone_number[1:]
    else:
        phone_number = '+91' + phone_number

    phone_number = phone_number[1:]

    return str(phone_number)

def generate_otp():
    otp = random.choice(range(100000,999999))
    return otp

def set_otp(phone_number):
    try:
        otp=generate_otp()
        redis_handler.set_redis_otp(phone_number=preprocess_phone_number(phone_number),otp=otp)
        return otp
    except Exception as e:
        raise Exception(f"Unable to set OTP, error {e}")
    
def validate_otp(phone_number,user_otp):
    stored_otp = redis_handler.get_redis_otp(phone_number=preprocess_phone_number(phone_number))
    print(stored_otp,user_otp)
    if stored_otp == 0:
        raise TimeoutError("OTP Expired Generate a New One")
    
    if stored_otp - user_otp == 0:
        return {
            "message":"Sucess",
            "Validation_success":True,
        }
    else:
        return {
            "message":"Declined",
            "Validation_success":False,
        }
    

if __name__ == "__main__":
    # print(preprocess_phone_number("07899404714"))
    # set_otp(phone_number="7899404714")

    print(validate_otp(phone_number="7899404714",user_otp=183855))