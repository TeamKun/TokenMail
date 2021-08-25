import random
import string

import gspread

from ideadiscord import sheet_constant

gc = gspread.oauth()

sh = gc.open_by_key(sheet_constant.sheet_id)
ws = sh.worksheet(sheet_constant.sheet_name)

selectorB = f'{sheet_constant.column_email}2:{sheet_constant.column_email}{ws.row_count}'

sample = ws.range(selectorB)
sa_count = max([cell.row for cell in sample if cell.value])
sh_count = sa_count - 1

selectorM = f'{sheet_constant.column_number_id}2:{sheet_constant.column_number_id}{sa_count}'
selectorN = f'{sheet_constant.column_token}2:{sheet_constant.column_token}{sa_count}'


def create_token(n):
    rands = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(rands)


ids = [[f'{i + 1}'] for i in range(sh_count)]
tokens = [[create_token(sheet_constant.num_token_length)] for i in range(sh_count)]

ws.update(selectorM, ids)
ws.update(selectorN, tokens)

print('完了')
