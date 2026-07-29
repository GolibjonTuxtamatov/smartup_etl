import requests
from config import get_headers, ENDPOINTS

row = requests.get(ENDPOINTS["inventory"],headers=get_headers())

row.json()