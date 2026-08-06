import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from os import getenv

load_dotenv()

_supa_user = getenv('SUPA_USER')
_supa_host = getenv('SUPA_BASE_HOST')
_supa_password = getenv('SUPA_PASSWORD')
_port = getenv('PORT')

SUPABASE_URL = f'postgresql://{_supa_user}:{_supa_password}@{_supa_host}:{_port}/postgres'

def load_to_supa_base(df: pd.DataFrame,table:str):


    if df.empty:
        print(f"{table} bo'sh!")
        return

    engine = create_engine(SUPABASE_URL)

    df.to_sql(
        name = table,
        con = engine,
        if_exists = 'replace',
        index = False
    )

    print(f"{table} {len(df)} ta qator yuklandi!")