from sqlalchemy import create_engine,text
import pandas as pd
try:
    from  .conf import *
except:
    from conf import *
import psycopg2




def create_connection():
    conn = psycopg2.connect(
    database=NAME , user=USER, password= PASSWORD, host=HOST , port= PORT
    )
    
    return conn

conn = create_connection()

def processquery(query: str) -> pd.DataFrame:
    conn = psycopg2.connect(
    database=NAME , user=USER, password= PASSWORD, host=HOST , port= PORT
    )

    """returns the query as pandas dataframe from database
    Args:
    --------
        query (str): query
    
    Returns:
    ---------
        data: pandas dataframe from query
    """
    table = pd.read_sql(query, con=conn)
    conn.close()
    return table

def excute_query(query:str,vars={}):

    global conn

    try:
        if conn.closed != 0:
            conn = create_connection()
        cursor = conn.cursor()   
        cursor.execute(query=query,vars=vars)
        conn.commit()
    except Exception as e:
        conn.close()
        raise Exception(e)
    
    
def excute_query_without_commit(cursor,query):
    try:
        cursor.execute(query=query)
    except Exception as e:
        raise Exception(e)



def excute_query_and_return_result(query:str,vars={}):
    try:
        global conn
   
        if conn.closed != 0:
            conn = create_connection()

        cursor = conn.cursor()   
        cursor.execute(query=query,vars=vars)
        data =  cursor.fetchall()

        return data
    except Exception as e:
        conn.close()
        raise Exception(e)

def update_sebi_ban(date_of_ban,symbol,sl,cursor):
    query = """INSERT INTO trade.sebi_ban_master (sl, date_of_ban, symbol)
    VALUES ("""+str(sl)+""", '"""+date_of_ban+"""', '"""+symbol+"""')
    ON CONFLICT (date_of_ban,symbol)
    DO UPDATE SET
        sl = EXCLUDED.sl;"""
    excute_query_without_commit(query=query,cursor=cursor)


def update_sebi_oi(date,symbol,mwpl,oi,cursor):
    query = """INSERT INTO trade.sebi_oi_master (date, symbol, mwpl,open_interest)
    VALUES ('"""+date+"""', '"""+symbol+"""', '"""+str(mwpl)+"""','"""+str(oi)+"""')
    ON CONFLICT (date,symbol)
    DO UPDATE SET
        mwpl = EXCLUDED.mwpl,
        open_interest = EXCLUDED.open_interest;"""
    
    
    excute_query_without_commit(query=query,cursor=cursor)

# print(processquery("SELECT * FROM public.user_logs"))
