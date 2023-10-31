from .dbcon import processquery,text,create_engine,excute_query,excute_query_and_return_result
from .conf import *
from .otp_handler import preprocess_phone_number



def handle_login(phone_number,password):
    phone_number = preprocess_phone_number(phone_number=phone_number)
    fetch_pass_query = f"select password,user_id,name from users.user_details where phone_number = '+{phone_number}'"   

    
    data = excute_query_and_return_result(fetch_pass_query)[0]
    if data is None:
        query = "insert into users.user_logs (user_id) values (0) returning id"
        excute_query_and_return_result(query=query)
        return 0,"No user found",404

    else:
        password_from_db,user_id,first_name = data
        if str(password_from_db) == str(password):
            query = f"insert into users.user_logs (user_id) values ({user_id}) returning id"
            excute_query(query=query)
            
            return user_id,f"Welcome {first_name}",200
        
        else:
            query = "insert into users.user_logs (user_id) values (0) returning id"
            excute_query(query=query)
            
            return 0,"Wrong Password",401
    

    
def log_user(request):

    headers = request.headers
    user_agent = headers['User-Agent']
    try:
        user_id = headers['uid-greed']
    except:
        user_id = 0

    query = f"insert into users.user_logs (user_id,user_agent) values ({user_id},'{user_agent}') returning id"

    excute_query(query=query)
      

    




if __name__ == '__main__':
    print(handle_login(phone_number=7899404714,password='12345678'))

    {
"phone_number":7899404714,
"password":12345678
}
