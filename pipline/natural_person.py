import sys
import os

# joriy fayldan bir papka yuqoriga (root'ga) chiqib, path'ga qo'shamiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import pandas as pd
from config import ENDPOINTS,get_headers
from extract import get_raw_data
from load import load_to_supa_base

# TODO extract
df = get_raw_data(ENDPOINTS['natural_person'],'natural_person',get_headers())

# TODO transform
df = df.loc[df['state'] == 'A'] 

df[['lat', 'lng']] = df['latlng'].str.split(',', expand=True)[[0, 1]]

# casting
df['lat'] = pd.to_numeric(df['lat'],errors='coerce').astype(float)
df['lng'] = pd.to_numeric(df['lng'],errors='coerce').astype(float)
df['person_id'] = pd.to_numeric(df['person_id'],errors='coerce').astype('int64')
df['birthday'] = pd.to_datetime(df['birthday'],format='mixed',errors='coerce')
# cleaning
df = df.drop_duplicates(subset=['person_id'])

# drop nested columns
natural_persons = df.drop(columns=['latlng','groups','rooms','delivery_addresses'])

#person groups
df_groups = []

for _,columns in df[['person_id','groups']].iterrows():
    personId = columns['person_id']

    for group in columns['groups']:
        group['person_id'] = personId

        df_groups.append(group)

natural_person_groups = pd.json_normalize(df_groups)

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
natural_person_rooms = df_rooms.drop_duplicates(subset=['room_id'])


#person delivery addresses
df_delivery_addresses = []

for _,columns in df[['person_id','delivery_addresses']].iterrows():
    personId = columns['person_id']

    for address in columns['delivery_addresses']:
        address['person_id'] = personId

        df_delivery_addresses.append(address)

df_delivery_addresses = pd.json_normalize(df_delivery_addresses)

# df_delivery_addresses[['lat', 'lng']] = df_delivery_addresses['latlng'].str.split(',', expand=True)[[0, 1]]
# df_delivery_addresses['lat'] = pd.to_numeric(df_delivery_addresses['lat'],errors='coerce').astype(float)
# df_delivery_addresses['lng'] = pd.to_numeric(df_delivery_addresses['lng'],errors='coerce').astype(float)

#cleaning duplicates
# legal_person_delivery_addresses = df_delivery_addresses.drop(columns=['latlng'])

natural_person_delivery_addresses = df_delivery_addresses

def print_text(table):
    print(f"{table} table is empty!")

#TODO LOAD
load_to_supa_base(natural_persons,'natural_persons') if not natural_persons.empty else print_text('natural_persons')
load_to_supa_base(natural_person_groups,'natural_person_groups') if not natural_person_groups.empty else print_text('natural_person_groups')
load_to_supa_base(natural_person_rooms,'natural_person_rooms') if not natural_person_rooms.empty else print_text('natural_person_rooms')
load_to_supa_base(natural_person_delivery_addresses,'natural_person_delivery_addresses') if not natural_person_delivery_addresses.empty else print_text('natural_person_delivery_addresses')