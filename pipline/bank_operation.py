import sys
import os

# joriy fayldan bir papka yuqoriga (root'ga) chiqib, path'ga qo'shamiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_headers,ENDPOINTS
from extract import get_raw_data
from operation import cleaning_operation,print_text
from load import load_to_supa_base

df = get_raw_data(ENDPOINTS['bank_operation'],'bank_operation',get_headers())


# cleaning and separate nested columns
bank_operation,ref_codes = cleaning_operation(df)

#LOAD
load_to_supa_base(bank_operation,'bank_operation') if not bank_operation.empty else print_text('bank_operation')
load_to_supa_base(ref_codes,'bank_ref_codes') if not ref_codes.empty else print_text('bank_ref_codes')
