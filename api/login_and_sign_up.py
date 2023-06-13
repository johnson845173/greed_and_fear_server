from .dbcon import processquery,text,create_engine
from .conf import *



def handle_login(phone_number,password):
    engine = create_engine(f'postgresql+psycopg2://{USER}:gtaVice%401a@{HOST}/{NAME}')
    fetch_pass_query = f"select password,user_id,first_name from public.user_details where phone_number = {phone_number}"
    engine = engine.connect()
    data = engine.execute(text(fetch_pass_query)).fetchone()
    print(data)
    if data is None:
        query = "insert into user_logs (user_id) values (0) returning id"
        id = engine.execute(text(query)).fetchone()
        print(id)
        return 0,"No user found"

    else:
        password_from_db,user_id,first_name = data
        if str(password_from_db) == str(password):
            query = f"insert into user_logs (user_id) values ({user_id}) returning id"
            id = engine.execute(text(query)).fetchone()
            print(id)
            return user_id,f"Welcome {first_name}"
        else:
            query = "insert into user_logs (user_id) values (0) returning id"
            id = engine.execute(text(query)).fetchone()
            print(id)
            return 0,"Wrong Password"
    

    




if __name__ == '__main__':
    print(handle_login(phone_number=7899404714,password='12345678'))

    {
"phone_number":7899404714,
"password":12345678
}
