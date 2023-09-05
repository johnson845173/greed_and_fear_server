from sqlalchemy import create_engine
import pandas as pd

connection_string = "mysql+mysqlconnector://tradebrains:Daily%40007Raven@206.189.130.194/portal"

engine = create_engine(connection_string, echo=True)

# with engine.connect() as con:
#     con.execute("""SELECT  * from portal.auth_user;""")

df = pd.read_sql(sql="SELECT * FROM portal.user_premiumuserfeedback;",con=engine)

print(df)

df.to_csv('prem_user_feedback.csv')
    
query = """select distinct((mobile::numeric)::bigint) as mobile,name,last_login,ud.id
from project_greed.user_data ud
join project_greed.dmat_data dd on dd.email = ud.email -- group by name

where is_superuser = '0'
	and is_staff = '0'
	and is_active = '1'
	and name is not null
	and last_login is not null
order by last_login desc"""

7107330