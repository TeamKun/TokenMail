import gspread
import string
import random

gc = gspread.oauth()

sh = gc.open_by_key("1QJmehI1eJDcYUAlDVulUe_P-gez_Xd6S5en0jk0A4B0")
ws = sh.worksheet('ユーザー')

selectorB = f'B3:B{ws.row_count}'

sample = ws.range(selectorB)
sa_count = max([cell.row for cell in sample if cell.value])
sh_count = sa_count - 2

selectorM = f'M3:M{sa_count}'
selectorN = f'N3:N{sa_count}'


def create_token(n):
    rands = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(rands)


ids = [[f'{i + 1}'] for i in range(sh_count)]
tokens = [[create_token(6)] for i in range(sh_count)]

ws.update(selectorM, ids)
ws.update(selectorN, tokens)

print('完了')
