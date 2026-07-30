import requests
import pandas as pd

def get_raw_data(url: str, key: str, headers: dict):

    print(f"{key} yuklanish boshlandi...")

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Xato status: {response.status_code}\n{response.text}")

    records = response.json().get(key) or []
    print(f"[OK] {len(records)} ta yozuv yuklandi.")

    if not records:
        return pd.DataFrame()

    return pd.json_normalize(records)
