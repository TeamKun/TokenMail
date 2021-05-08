import gspread
import string
import random

gc = gspread.oauth()

sh = gc.open_by_key("1QJmehI1eJDcYUAlDVulUe_P-gez_Xd6S5en0jk0A4B0")
ws = sh.worksheet('第2回通過者')

selectorB = f'B2:B{ws.row_count}'

sample = ws.range(selectorB)
sa_count = max([cell.row for cell in sample if cell.value])
sh_count = sa_count - 1

selectorM = f'P2:P{sa_count}'
selectorN = f'Q2:Q{sa_count}'


def create_token(n):
    rands = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(rands)


ids = [[f'{i + 1}'] for i in range(sh_count)]
tokens = [[create_token(7)] for i in range(sh_count)]

ws.update(selectorM, ids)
ws.update(selectorN, tokens)

print('完了')
