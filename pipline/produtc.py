import pandas as pd
from config import get_headers,ENDPOINTS
from client import get_raw_data

def run_clean_product() -> pd.DataFrame:
    df_products = get_raw_data(ENDPOINTS['inventory'],'inventory',get_headers())

    df_product_groups = df_products[['product_id','groups']]
    df_product_inventory_kinds = df_products[['product_id','inventory_kinds']]
    df_product_sector_codes = df_products[['product_id','sector_codes']]

    df_products = df_products.drop(columns=['groups','inventory_kinds','sector_codes'])

    for column in df_products:
        if df_products[column].isnull().sum() > len(df_products)/2:
            df_products.drop(columns=column,inplace=True)

    df_products['code'] = pd.to_numeric(df_products['code'],errors='coerce')
    df_products['measure_code'] = pd.to_numeric(df_products['measure_code'],errors='coerce')

    for column in df_products.columns:
        if df_products[column].dtype == 'object':
            df_products[column] = df_products[column].fillna('none')
        elif pd.api.types.is_numeric_dtype(df_products[column]):
            df_products[column] = df_products[column].fillna(0)

    return df_product_groups
