import sys
import os

# joriy fayldan bir papka yuqoriga (root'ga) chiqib, path'ga qo'shamiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import pandas as pd
from config import ENDPOINTS,get_headers
from extract import get_raw_data
from load import load_to_supa_base

# TODO extract
df = get_raw_data(ENDPOINTS['legal_person'],'legal_person',get_headers())

# TODO transform
df = df.loc[df['state'] == 'A'] 

df[['lat', 'lng']] = df['latlng'].str.split(',', expand=True)[[0, 1]]

# casting
df['lat'] = pd.to_numeric(df['lat'],errors='coerce').astype(float)
df['lng'] = pd.to_numeric(df['lng'],errors='coerce').astype(float)
df['person_id'] = pd.to_numeric(df['person_id'],errors='coerce').astype('int64')

# cleaning
df = df.drop_duplicates(subset=['person_id'])

# drop nested columns
legal_persons = df.drop(columns=['latlng','groups','bank_accounts','rooms','delivery_addresses'])

#person groups
df_groups = []

for _,columns in df[['person_id','groups']].iterrows():
    personId = columns['person_id']

    for group in columns['groups']:
        group['person_id'] = personId

        df_groups.append(group)

df_groups = pd.json_normalize(df_groups)

#cast nameric
df_groups['group_id'] = pd.to_numeric(df_groups['group_id'],errors='coerce').astype('int64')
df_groups['type_id'] = pd.to_numeric(df_groups['type_id'],errors='coerce').astype('int64')

#cleaning duplicates
legal_person_groups = df_groups.drop_duplicates(subset=['group_id','type_id'])

#person bank accounts
df_accounts = []

for _,columns in df[['person_id','bank_accounts']].iterrows():
    personId = columns['person_id']

    for account in columns['bank_accounts']:
        account['person_id'] = personId

        df_accounts.append(account)

df_accounts = pd.json_normalize(df_accounts)

#cast nameric
df_accounts['bank_account_id'] = pd.to_numeric(df_accounts['bank_account_id'],errors='coerce').astype('int64')

#cleaning duplicates
legal_person_bank_accounts = df_accounts.drop_duplicates(subset=['bank_account_id'])

#person rooms
df_rooms = []

for _,columns in df[['person_id','rooms']].iterrows():
    personId = columns['person_id']

    for room in columns['rooms']:
        room['person_id'] = personId

        df_rooms.append(room)

df_rooms = pd.json_normalize(df_rooms)

#cast nameric
df_rooms['room_id'] = pd.to_numeric(df_rooms['room_id'],errors='coerce').astype('int64')

#cleaning duplicates
legal_person_rooms = df_rooms.drop_duplicates(subset=['room_id'])


#person delivery addresses
df_delivery_addresses = []

for _,columns in df[['person_id','delivery_addresses']].iterrows():
    personId = columns['person_id']

    for address in columns['delivery_addresses']:
        address['person_id'] = personId

        df_delivery_addresses.append(address)

df_delivery_addresses = pd.json_normalize(df_delivery_addresses)

df_delivery_addresses[['lat', 'lng']] = df_delivery_addresses['latlng'].str.split(',', expand=True)[[0, 1]]
df_delivery_addresses['lat'] = pd.to_numeric(df_delivery_addresses['lat'],errors='coerce').astype(float)
df_delivery_addresses['lng'] = pd.to_numeric(df_delivery_addresses['lng'],errors='coerce').astype(float)

#cleaning duplicates
legal_person_delivery_addresses = df_delivery_addresses.drop(columns=['latlng'])

def print_text(table):
    print(f"{table} table is empty!")

#TODO LOAD
load_to_supa_base(legal_persons,'legal_persons') if not legal_persons.empty else print_text('legal_persons')
load_to_supa_base(legal_person_groups,'legal_person_groups') if not legal_person_groups.empty else print_text('legal_person_groups')
load_to_supa_base(legal_person_rooms,'legal_person_rooms') if not legal_person_rooms.empty else print_text('legal_person_rooms')
load_to_supa_base(legal_person_bank_accounts,'legal_person_bank_accounts') if not legal_person_bank_accounts.empty else print_text('legal_person_bank_accounts')
load_to_supa_base(legal_person_delivery_addresses,'legal_person_delivery_addresses') if not legal_person_delivery_addresses.empty else print_text('legal_person_delivery_addresses')