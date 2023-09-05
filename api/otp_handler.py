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
    otp=generate_otp()
    redis_handler.set_redis_otp(phone_number=preprocess_phone_number(phone_number),otp=otp)


def validate_otp(phone_number,user_otp):
    pass
    # # Extract phone number from a string
    # extract_phone_number_pattern = "\\+?[1-9][0-9]{7,14}"
    # result = re.findall(extract_phone_number_pattern, 'You can reach me out at +12223334444 and +56667778888') # returns ['+12223334444', '+56667778888']

    # print(result)

if __name__ == "__main__":
    # print(preprocess_phone_number("07899404714"))
    print(set_otp(phone_number="7899404714"))