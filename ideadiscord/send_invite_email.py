import base64
import os
from email.mime.text import MIMEText
from email.utils import formataddr

import gspread
from apiclient import errors
from googleapiclient.discovery import build

from ideadiscord import sheet_constant

# 1. Gmail APIのスコープを設定
GMAIL_DEFAULT_SCOPES = gspread.auth.DEFAULT_SCOPES + ['https://www.googleapis.com/auth/gmail.send']

# 招待リンク
INVITE_LINK = os.environ["DISCORD_INVITE_LINK"]

# Spread Sheet
gc = gspread.oauth(GMAIL_DEFAULT_SCOPES)

sh = gc.open_by_key(sheet_constant.sheet_id)
ws = sh.worksheet(sheet_constant.sheet_name)


# 2. メール本文の作成
def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = formataddr(('KUN Lab採用 (かめすた)', 'kamesuta@gmail.com'))
    message['subject'] = subject
    encode_message = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': encode_message.decode()}


# 3. メール送信の実行
def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


# 5. アクセストークンの取得
service = build('gmail', 'v1', credentials=gc.auth)


def send_invite_email(to, user_name, user_token):
    # 6. メール本文の作成
    subject = '[第2回 KUN Lab選考] 選考通過と、Discordへの参加について'
    message_text = f'''\
{user_name} 様

このたびは第2回 KUN Lab選考にご応募いただきありがとうございます。
試験の結果、二次試験にお進みいただきたくご連絡差し上げました。

ついては、Discordの参加をご案内させていただきます。
下記のリンクからご参加いだだいた後、Discord内の案内に従い下記の認証コードの入力をお願いします。

▼ Discord招待URL
{INVITE_LINK}

▼ あなたの認証コード (6桁)
{user_token}
※注意 認証コードを他の人に教えないでください。

-------------------------------------------------------
KUN Lab
採用担当：かめすた
E-mail　 kamesuta@gmail.com
Twitter　https://twitter.com/Kmesuta
-------------------------------------------------------
'''
    message = create_message(to, subject, message_text)

    # 7. Gmail APIを呼び出してメール送信
    send_message(service, 'me', message)


selectorB = f'{sheet_constant.column_email}2:{sheet_constant.column_email}{ws.row_count}'

sample = ws.range(selectorB)
sa_count = max([cell.row for cell in sample if cell.value])
sh_count = sa_count - 1

selectorB = f'{sheet_constant.column_email}2:{sheet_constant.column_email}{sa_count}'
selectorD = f'{sheet_constant.column_real_name}2:{sheet_constant.column_real_name}{sa_count}'
selectorN = f'{sheet_constant.column_token}2:{sheet_constant.column_token}{sa_count}'

users = ws.batch_get([selectorB, selectorD, selectorN])

for i in range(sh_count):
    user_email = users[0][i][0]
    user_name = users[1][i][0]
    user_token = users[2][i][0]

    send_invite_email(user_email, user_name, user_token)
    print(f'Email:{user_email}, ID:{user_name}, Token:{user_token}')
