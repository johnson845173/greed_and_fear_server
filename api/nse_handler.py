import datetime
import re
import os
import zipfile
import glob
import requests

import pandas as pd

try:
    from . import dbcon
except:
    import dbcon

columns_to_rename = {
    "Date": "date",
    "nse symbol": "symbol",
    "nse open interest": "open_interest"
}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0. 9",
    "Referer": "https//www.nseindia.com/",
    "Sec-Ch-Ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    "Sec-Ch-Ua-Mobile": "?1",
    "Sec-Ch-Ua-Platform": '"Android"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
}


def get_oi_sebi():

    open_intrest_url = "https://archives.nseindia.com/content/nsccl/nseoi.zip"

    data = requests.get(url=open_intrest_url, headers=headers, timeout=10)

    with open('oi.zip', 'wb') as file:
        file.write(data.content)

    with zipfile.ZipFile('oi.zip', 'r') as zip_ref:
        zip_ref.extractall('oi')

    csv_file = glob.glob(os.path.join("oi", "*.csv"))[0]

    df = pd.read_csv(csv_file)

    df.rename(columns=lambda x: x.strip().lower(), inplace=True)

    df.rename(columns=columns_to_rename, inplace=True)

    df = df[['date', 'symbol', 'mwpl', 'open_interest']]



    conn, cursor = dbcon.create_connection()

    for index, row in df.iterrows():
        print(f"{index+1}/{df.shape[0]}")
        parsed_date = datetime.datetime.strptime(row['date'], "%d-%b-%Y")
        formatted_date = parsed_date.strftime("%Y-%m-%d")
        dbcon.update_sebi_oi(date=formatted_date, symbol=row['symbol'],
                             mwpl=row['mwpl'], oi=row['open_interest'], cursor=cursor)

    conn.commit()
    conn.close()

    files = os.listdir('oi')
    # Iterate through the files and delete each one
    for file_name in files:
        file_path = os.path.join('oi', file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")


def get_sebi_bans():

    sebi_bans_url = "https://nsearchives.nseindia.com/content/fo/fo_secban.csv"

    data = requests.get(url=sebi_bans_url, headers=headers, timeout=10)
    
    with open("bans.csv", 'wb') as file:
        file.write(data.content)

    no_skip_df = pd.read_csv("bans.csv")

    df = pd.read_csv("bans.csv", skiprows=1, names=['sl', 'symbol'])

    conn, cursor = dbcon.create_connection()

    title = no_skip_df.columns.values[0]

    print(title)

    pattern = r"Trade Date (\d{2}-[A-Z]{3}-\d{4}):"

    match = re.search(pattern, title)

    if match:
        trade_date = match.group(1)
    else:
        raise Exception("Date not found.")

    date_format = "%d-%b-%Y"

    date_of_ban = datetime.datetime.strptime(
        trade_date, date_format).strftime("%Y-%m-%d")

    for index, row in df.iterrows():

        dbcon.update_sebi_ban(
            cursor=cursor, date_of_ban=date_of_ban, sl=row['sl'], symbol=row['symbol'])

    conn.commit()
    conn.close()

def get_sebi_bans_method():

    sebi_bans_url = "https://nsearchives.nseindia.com/content/fo/fo_secban.csv"

    data = requests.get(url=sebi_bans_url, headers=headers, timeout=10)

    with open("bans.csv", 'wb') as file:
        file.write(data.content)

    no_skip_df = pd.read_csv("bans.csv")

    df = pd.read_csv("bans.csv", skiprows=1, names=['sl', 'symbol'])


    title = no_skip_df.columns.values[0]

    pattern = r"Trade Date (\d{2}-[A-Z]{3}-\d{4}):"

    match = re.search(pattern, title)

    if match:
        trade_date = match.group(1)
    else:
        raise Exception("Date not found.")

    date_format = "%d-%b-%Y"

    date_of_ban = datetime.datetime.strptime(trade_date, date_format).strftime("%Y-%m-%d")

    data_to_send = {
        "date_of_ban":date_of_ban,
        "stock_list":df['symbol'].to_list()
    }

    return data_to_send

def get_nse_bans_from_data_base(date_of_trade="",date_to_compare=""):
    query = f"""with today_ban as
        (select symbol as today_symbol,
                date_of_ban as today_date_of_ban
            from trade.sebi_ban_master
            where date_of_ban = '{date_of_trade}'),
        yesterday_ban as
        (select symbol,
                date_of_ban
            from trade.sebi_ban_master
            where date_of_ban = '{date_to_compare}'),
        ban_data as
        (select *
            from today_ban tb
            full outer join yesterday_ban yb on tb.today_symbol = yb.symbol)
            
    select 
    case
    when today_date_of_ban is null then symbol::text
    when date_of_ban is null then today_symbol::text
    when date_of_ban is not null and today_date_of_ban is not null then today_symbol::text
    end Stock
    ,
    case
    when today_date_of_ban is null then 'Unbanned'::text
    when date_of_ban is null then 'New Ban'::text
    when date_of_ban is not null and today_date_of_ban is not null then 'Ban Continue'::text
    end ban_status
    from ban_data"""
    
    print(query)
    df = dbcon.processquery(query=query)
    
    new_ban = df.loc[df['ban_status'] == 'New Ban']['stock'].to_list()
    ban_con = df.loc[df['ban_status'] == 'Ban Continue']['stock'].to_list()
    un_ban = df.loc[df['ban_status'] == 'Unbanned']['stock'].to_list()

    ban_data_to_send = {
        "date_of_trade":date_of_trade,
        "date_to_compare":date_to_compare,
        "unbanned":un_ban,
        "ban_continue":ban_con,
        "new_ban":new_ban,
    }

    return ban_data_to_send

if __name__ == '__main__':
    # print(get_sebi_bans_method())
    get_oi_sebi()
    # get_sebi_bans()
    # get_nse_bans_from_data_base()
