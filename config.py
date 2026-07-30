from dotenv import load_dotenv
import base64
import os

load_dotenv()

_login = os.getenv('LOGIN')
_password = os.getenv('PASSWORD')
_project_code = os.getenv('PROJECT_CODE')
_filial_id = os.getenv('FILIAL_ID')

# endpoints
ENDPOINTS = {
    "inventory": "https://smartup.online/b/anor/mxsx/mr/inventory$export",
    "legal_person": "https://smartup.online/b/anor/mxsx/mr/legal_person$export",
    "natural_person": "https://smartup.online/b/anor/mxsx/mr/natural_person$export",
    "order": "https://smartup.online/b/trade/txs/tdeal/order$export",
    "payment_from_client": "https://smartup.online/b/trade/txs/tcs/cashin$export",
    "cash_operation": "https://smartup.online/b/anor/mxsx/mkcs/cash_operation$export",
    "bank_operation": "https://smartup.online/b/anor/mxsx/mkcs/bank_operation$export"
}


def get_headers() -> dict:
    encode = base64.b64encode(f"{_login}:{_password}".encode()).decode()

    return {
        'Authorization': f"Basic {encode}",
        'project_code': _project_code,
        'filial_id': _filial_id
    }

