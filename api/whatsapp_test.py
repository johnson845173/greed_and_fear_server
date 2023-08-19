import requests

try:
    from .dbcon import excute_query_and_return_result

except:
    from dbcon import excute_query_and_return_result

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


def send_media_by_whatsapp_api(phone_number,message,url):

    url  = "https://flyencart.com/api/send"

    pay_load = {
        "number": phone_number,
        "type": "media",
        "message": message,
        "media_url": "{string}",
        "instance_id": "64E0706F523C7",
        "access_token": "64dde5ca2cc72"
    }



    data = requests.post(url=url,data=pay_load)

    print(data.json())


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

if __name__ == "__main__":
    send_sub_renew_message(user_id=1)