
from dotenv import load_dotenv
import os

load_dotenv()

NAME = os.getenv('NAME')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

bottoken = os.getenv('bottoken')

