from .dbcon import processquery,text,create_engine
from .conf import *



def handle_login(phone_number,password):
    engine = create_engine(f'postgresql+psycopg2://{USER}:gtaVice%401a@{HOST}:{PORT}/{NAME}')
    fetch_pass_query = f"select password,user_id,first_name from public.user_details where phone_number = {phone_number}"
    engine = engine.connect()
    
    data = engine.execute(text(fetch_pass_query)).fetchone()
    if data is None:
        query = "insert into user_logs (user_id) values (0) returning id"
        id = engine.execute(text(query)).fetchone()
        engine.dispose()
        print(id)
        return 0,"No user found"

    else:
        password_from_db,user_id,first_name = data
        if str(password_from_db) == str(password):
            query = f"insert into user_logs (user_id) values ({user_id}) returning id"
            print(query)
            id = engine.execute(text(query)).fetchone()
            engine.dispose()
            return user_id,f"Welcome {first_name}"
        
        else:
            query = "insert into user_logs (user_id) values (0) returning id"
            id = engine.execute(text(query)).fetchone()
            print(id)
            engine.dispose()
            return 0,"Wrong Password"
    

    
def log_user(request):
    engine = create_engine(f'postgresql+psycopg2://{USER}:gtaVice%401a@{HOST}:{PORT}/{NAME}')

    headers = request.headers
    user_agent = headers['User-Agent']
    try:
        user_id = headers['uid-greed']
        query = f"insert into user_logs (user_id,user_agent) values ({user_id},'{user_agent}') returning id"
        engine.execute(text(query)).fetchone()
    except:
        query = f"insert into user_logs (user_id,user_agent) values (0,'{user_agent}') returning id"
        engine.execute(text(query)).fetchone()
    
    

    




if __name__ == '__main__':
    print(handle_login(phone_number=7899404714,password='12345678'))

    {
"phone_number":7899404714,
"password":12345678
}
