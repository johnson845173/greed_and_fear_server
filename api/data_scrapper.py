from dbcon import processquery,psycopg2,engine,excute_query
import pandas as pd

df = pd.read_excel("project_greed/i (2).xlsx",sheet_name="175800")

df.rename(columns = lambda x: x.strip().lower(), inplace = True)

columns_to_be_rename = {
        "user name":"user_name",
        "email id":"email",
        "mobile no.":"mobile",
        "address":"adress"
}

df.rename(columns=columns_to_be_rename,inplace = True)

print(df)

df = df[['user_name','email','mobile','adress']]

df.to_sql(name="insta_user_data",schema="project_greed",con=engine,if_exists='append',index=False)

print(df)