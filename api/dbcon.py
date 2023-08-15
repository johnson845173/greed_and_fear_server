from sqlalchemy import create_engine,text
import pandas as pd
from  .conf import *
import psycopg2


engine = create_engine(f'postgresql+psycopg2://{USER}:gtaVice%401a@{HOST}/{NAME}')

# conn = psycopg2.connect(
#     database=NAME , user=USER, password= PASSWORD, host=HOST , port= PORT
#     )

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

def excute_query(query:str):
    try:
        conn = psycopg2.connect(
    database=NAME , user=USER, password= PASSWORD, host=HOST , port= PORT
    )

        cursor = conn.cursor()   
        cursor.execute(query=query)
    except Exception as e:
        print(e)
        raise Exception(e)
    finally:
        conn.commit()
        conn.close()

# print(processquery("SELECT * FROM public.user_logs"))
