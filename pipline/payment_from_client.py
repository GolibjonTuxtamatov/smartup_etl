import sys
import os

# joriy fayldan bir papka yuqoriga (root'ga) chiqib, path'ga qo'shamiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from config import get_headers,ENDPOINTS
from extract import get_raw_data
from load import load_to_supa_base

df = get_raw_data(ENDPOINTS['payment_from_client'],'payment_from_client',get_headers())

#cast namerics
int_columns = ['cashin_id','client_id']

#casting
for column in int_columns:
    df[column] = pd.to_numeric(df[column],errors='coerce').astype('int64')

df['amount'] = pd.to_numeric(df['amount'],errors='coerce')

payments = df.drop_duplicates(subset=['cashin_id'])

#LOAD
load_to_supa_base(payments,'payments') if not payments.empty else print("payments table is empty")
