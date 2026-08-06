import sys
import os

# joriy fayldan bir papka yuqoriga (root'ga) chiqib, path'ga qo'shamiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from config import get_headers,ENDPOINTS
from extract import get_raw_data
from load import load_to_supa_base

df = get_raw_data(ENDPOINTS['inventory'],'inventory',get_headers())

# TODO: Transform

df = df[df['state'] == 'A']

# Cast numerics
int_columns = ['product_id']
float_columns = ["weight_netto", "weight_brutto", "litr", "box_quant", "order_no"]

for col in int_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
 
for col in float_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# drop duplicate
products = df.drop_duplicates(subset=["product_id"])
# nested ustunlarni olib tashlaymiz - to_sql list/dict ni yozolmaydi
products = products.drop(columns=['groups', 'inventory_kinds', 'sector_codes'])


# products_group
group_rows = []
for _, row in df[['product_id', 'groups']].iterrows():
    # break
    pid = row["product_id"]
    for g in row["groups"] or []:
        group_rows.append({
            "product_id"  : pid,
            "group_id"    : g.get("group_id"),
            "group_code"  : g.get("group_code"),
            "type_id"     : g.get("type_id"),
            "type_code"   : g.get("type_code"),
        })
products_group = pd.json_normalize(group_rows) if group_rows else pd.DataFrame(
    columns=["product_id", "group_id", "group_code", "type_id", "type_code"]
)

if len(products_group):
    products_group["product_id"] = pd.to_numeric(products_group["product_id"], errors="coerce").astype("Int64")
    products_group["group_id"]   = pd.to_numeric(products_group["group_id"],   errors="coerce").astype("Int64")
    products_group["type_id"]    = pd.to_numeric(products_group["type_id"],    errors="coerce").astype("Int64")
    products_group = products_group.drop_duplicates(subset=["product_id", "group_id", "type_id"])

# product_inv_kind 
inv_rows = []
for _, row in df[["product_id", "inventory_kinds"]].iterrows():
    pid = row["product_id"]
    for item in row["inventory_kinds"] or []:
        ik = item.get("inventory_kind")
        if ik:
            inv_rows.append({"product_id": pid, "inventory_kind": ik.strip().upper()})
 
product_inv = pd.DataFrame(inv_rows) if inv_rows else pd.DataFrame(
    columns=["product_id", "inventory_kind"]
)

if len(product_inv):
    product_inv["product_id"] = pd.to_numeric(product_inv["product_id"], errors="coerce").astype("Int64")
    product_inv = product_inv.drop_duplicates(subset=["product_id", "inventory_kind"])

# product_sector
sector_rows = []
for _, row in df[["product_id", "sector_codes"]].iterrows():
    pid = row["product_id"]
    for item in row["sector_codes"] or []:
        sc = item.get("sector_code")
        if sc:
            sector_rows.append({"product_id": pid, "sector_code": str(sc).strip()})
 
product_sector = pd.DataFrame(sector_rows) if sector_rows else pd.DataFrame(
    columns=["product_id", "sector_code"]
)

if len(product_sector):
    product_sector["product_id"] = pd.to_numeric(product_sector["product_id"], errors="coerce").astype("Int64")
    product_sector = product_sector.drop_duplicates(subset=["product_id", "sector_code"])

# TODO: Load
load_to_supa_base(products, 'products')
load_to_supa_base(products_group, 'products_group')
load_to_supa_base(product_inv, 'product_inv')
load_to_supa_base(product_sector, 'product_sector')
