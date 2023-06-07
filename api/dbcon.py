from sqlalchemy import create_engine,text
import pandas as pd
from conf import *

engine = create_engine(f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}/{NAME}')

