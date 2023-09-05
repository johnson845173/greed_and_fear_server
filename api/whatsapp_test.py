import requests
import time
import random

try:
    from .dbcon import excute_query_and_return_result,processquery,excute_query
    from .otp_handler import preprocess_phone_number

except:
    from dbcon import excute_query_and_return_result,processquery,excute_query
    from otp_handler import preprocess_phone_number

def send_message_by_whatsapp_api(phone_number,message):
    url  = "https://flyencart.com/api/send/"

    pay_load = {
        "number": phone_number,
        "type": "text",
        "message": message,
        "instance_id": "64E0706F523C7",
        "access_token": "64dde5ca2cc72"
    }



    data = requests.post(url=url,data=pay_load)

    print(data.json())

def send_whatsapp_otp_message(phone_number,otp):
    message_format = f"Dear customer, use this One Time Password {otp} to create your Greed And Fear account. This OTP will be valid for the next 5 mins."
    send_message_by_whatsapp_api(phone_number=phone_number,message=message_format)


def send_media_by_whatsapp_api(phone_number,message,img_url):

    url  = "https://flyencart.com/api/send/"

    pay_load = {
        "number": phone_number,
        "type": "",
        "message": message,
        "media_url": f"{img_url}",
        "filename":"bn.jpg",
        "instance_id": "64E899A929C49",
        "access_token": "64dde5ca2cc72"
    }



    data = requests.post(url=url,data=pay_load,timeout=10)


    # print(data.content)


def send_sub_renew_message(user_id):

    query = f"select name,phone_number from users.user_details where user_id = {user_id}"
    user_details = excute_query_and_return_result(query=query)
    if len(user_details) == 0:
        raise Exception("No user found")
    name,phone_number = user_details[0]
    phone_number = phone_number[1:]
    
    message = f"Hey {name} \nTeam Greed and Fear here \n\nYour Subscription is about to end today. Click on below link to Renew it\n\n www.greedandfear.fun/productpage.html "
    # print(message)
    send_message_by_whatsapp_api(phone_number=phone_number,message=message)


def send_whatsapp_promo(name,phone_number):
    message = f"""Hey, {name} 
Team GREED & FEAR offers highly accurate Elliott Wave, Fibonacci, and Advance price action setups with exceptional risk-to-reward ratios. Join our esteemed community to learn and trade scalping, intraday, and short-term (swing) setups in stocks, commodities, and indices with in-depth explanations of logic and psychology behind every setups.

*Free Telegram Link*: 
https://t.me/GREEDandFEAR725

 *Website Link*: 
www.greedandfear.fun

 *Instagram Link*: 
http://surl.li/kjmgq 
        """
            

    img_url = "https://s3.greedandfear.fun/products/ash.jpg"
    # send_media_by_whatsapp_api(phone_number=)

    send_media_by_whatsapp_api(phone_number=phone_number,message=message,img_url=img_url)
    

def send_promo():
    query = """select distinct((mobile::numeric)::bigint) as mobile,concat(first_name,' ',last_name ) as name,last_login,ud.id,city
    from project_greed.user_data ud
    join project_greed.dmat_data dd on dd.email = ud.email -- group by name

    where is_superuser = '0'
        and is_staff = '0'
        and is_active = '1'
        and name is not null
        and last_login is not null and city like 'Bangalore%' and ud.sent = 'false'
    order by last_login desc
        """

    df = processquery(query=query)
    for index,row in df.iterrows():
        print(f"{index+1}/{df.shape[0]}")
        id = row['id']
        name = row['name']
        phone = row['mobile']
        try:
            send_whatsapp_promo(name=name,phone_number=preprocess_phone_number(str(phone)))
            # send_whatsapp_promo(name=name,phone_number="917760450407")
            # break
            update_query = f"update project_greed.user_data set sent = 'true' where id = '{id}'"
            excute_query(query=update_query)
            print(name,preprocess_phone_number(phone),"sucsess")
        except Exception as e: 
            print(name,preprocess_phone_number(phone),"failed")
        # break
        i = random.choice(range(5,30))
        print(i,"daelay")
        time.sleep(i)

if __name__ == "__main__":
    send_promo()
    # send_sub_renew_message(user_id=13)
    # send_whatsapp_otp_message("916363941989",otp="894537")
    