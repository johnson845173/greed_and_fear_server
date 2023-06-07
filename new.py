from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import json
import requests
from bs4 import BeautifulSoup


def get_token():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", False)
    driver = webdriver.Chrome(options=options)

    driver.maximize_window()

    data = driver.get(f"https://web.sensibull.com/option-strategy-builder?instrument_symbol=AMBUJACEM")

    print(data)

get_token()