import sys
import os

# joriy fayldan bir papka yuqoriga (root'ga) chiqib, path'ga qo'shamiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import pandas as pd
from config import get_headers,ENDPOINTS
from extract import get_raw_data
from load import load_to_supa_base


df = get_raw_data(ENDPOINTS['order'],'order',get_headers())

#cast nameric
int_columns = ['filial_id','deal_id','delivery_number','room_id','person_id','modified_id']
float_columns = ['total_amount','total_weight_netto','total_weight_brutto','total_litre']


for column in int_columns:
    df[column] = pd.to_numeric(df[column],errors='coerce').astype('int64')

for column in float_columns:
    df[column] = pd.to_numeric(df[column],errors='coerce')

#cast datetime
df['deal_time'] = pd.to_datetime(df['deal_time'],errors='coerce')
df['delivery_date'] = pd.to_datetime(df['delivery_date'],errors='coerce')
df['booked_date'] = pd.to_datetime(df['booked_date'],errors='coerce')

#drop duplicates
orders = df.drop_duplicates(subset=['deal_id'])

#drop nested columns
orders = orders.drop(columns=['order_products','order_gifts','order_actions','order_consignments'])

#order_items
order_items = []
order_item_details = []
order_item_action_margins = []

for _,item in df[['deal_id','order_products']].iterrows():

    # print(item['order_products'])

    #attach order id
    orderId = item['deal_id']

    #get products in orders like order items
    for order_item in item['order_products']:

            #attach order item id
            order_item_id = order_item['product_unit_id']

            order_details = order_item['details']
            order_action_margins = order_item['action_margins']

            order_item['deal_id'] = orderId

            order_item.pop('details',None)
            order_item.pop('action_margins',None)

            order_items.append(order_item)

            #get order item details
            if len(order_details):
                    for order_detail in order_details:
                          order_detail['prodcut_unit_id'] = order_item_id

                          order_item_details.append(
                                order_detail
                          )

            #get order item action margins
            if len(order_action_margins):
                    for action_margin in order_action_margins:
                        action_margin['prodcut_unit_id'] = order_item_id

                        order_item_action_margins.append(
                             action_margin 
                        )


#casting order items
order_items = pd.json_normalize(order_items)

if not order_items.empty:
    order_items_int_columns = ['product_unit_id','product_id','price_type_id']
    order_items_float_columns = ['order_quant','return_quant','product_price','margin_amount','margin_value','sold_quant','sold_amount']

    for col in order_items_int_columns:
        order_items[col] = pd.to_numeric(order_items[col],errors='coerce').astype('int64')

    for col in order_items_float_columns:
        order_items[col] = pd.to_numeric(order_items[col],errors='coerce')

    order_items = order_items.drop_duplicates(subset=['deal_id'])
    
#casting order item details
order_item_details = pd.json_normalize(order_item_details)

if not order_item_details.empty:
    order_item_details['prodcut_unit_id'] = pd.to_numeric(order_item_details['prodcut_unit_id'],errors='coerce').astype('int64')
    order_item_details.drop_duplicates(subset=['prodcut_unit_id'])

#casting order item action margins
order_item_action_margins = pd.json_normalize(order_item_action_margins)

if not order_item_action_margins.empty:
     pass

def print_text(table):
     print(f"{table} table bo'sh!")

#LOAD
load_to_supa_base(orders,'orders') if not orders.empty else print_text("order")
load_to_supa_base(order_items,'order_items') if not order_items.empty else print_text("order_items")
load_to_supa_base(order_item_details,'order_item_details') if not order_item_details.empty else print_text("order_item_details")
load_to_supa_base(order_item_action_margins,'order_item_action_margins') if not order_item_action_margins.empty else print_text("order_item_action_margins")

