from dotenv import load_dotenv
import base64
import os

load_dotenv()

login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')
project_code = os.getenv('PROJECT_CODE')
filial_id = os.getenv('FILIAL_ID')

# endpoints
ENDPOINTS = {
    "inventory": "https://smartup.online/b/anor/mxsx/mr/inventory$export",
    "legal_person": "https://smartup.online/b/anor/mxsx/mr/legal_person$export",
    "natural_person": "https://smartup.online/b/anor/mxsx/mr/natural_person$import",
    "order": "https://smartup.online/b/trade/txs/tdeal/order$import",
    "payment_from_client": "https://smartup.online/b/trade/txs/tcs/cashin$import",
    "cash_operation": "https://smartup.online/b/anor/mxsx/mkcs/cash_operation$import",
    "bank_operation": "https://smartup.online/b/anor/mxsx/mkcs/bank_operation$import"
}


def get_headers() -> dict:
    encode = base64.b64encode(f"{login}:{password}".encode()).decode()

    return {
        'Authorization': f"Basic {encode}",
        'project_code': project_code,
        'filial_id': filial_id
    }

