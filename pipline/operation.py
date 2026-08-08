import pandas as pd

def cleaning_operation(df:pd.DataFrame):

    #cast nameric
    df['operation_id'] = pd.to_numeric(df['operation_id'],errors='coerce').astype('int64')
    df['amount'] = pd.to_numeric(df['amount'],errors='coerce')
    df['operation_date'] = pd.to_datetime(df['operation_date'],errors='coerce')

    #separate nested ref_codes table
    ref_rows = df[['operation_id','ref_codes']]

    df = df.drop_duplicates(subset=['operation_id'])

    #delete nested column
    operation = df.drop(columns=['ref_codes'])

    ref_codes = []

    for _,refs in ref_rows.iterrows():

        operationId = refs['operation_id']

        for ref in refs['ref_codes']:
            ref['operation_id'] = operationId
            ref_codes.append(ref)


    ref_codes = pd.json_normalize(ref_codes)

    ref_codes['ref_id'] = pd.to_numeric(ref_codes['ref_id'],errors='coerce').astype('int64')

    return operation,ref_codes

def print_text(table):
    print(f"{table} table is empty!")