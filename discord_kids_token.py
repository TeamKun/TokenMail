import datetime
import os
import random
import string

import discord
from discord.ext import commands
import gspread
from discord_slash import SlashCommand
from discord_slash import SlashContext

# 認証チャンネルサーバー
REQUEST_SERVER_ID = 590731095817846784
# 認証チャンネル
REQUEST_CHANNEL_ID = 592669590061056010
USE_CHANNEL_ID = 792794338336964620
# ロール
ROLE_ID = 811764885784494091
# 招待リンク
INVITE_LINK = os.environ["DISCORD_INVITE_LINK"]

# Spread Sheet
gc = gspread.oauth()

sh = gc.open_by_key("1QJmehI1eJDcYUAlDVulUe_P-gez_Xd6S5en0jk0A4B0")
ws = sh.worksheet('参加勢')

# Discord
client = commands.Bot('/')
slash = SlashCommand(client)


@client.event
async def on_ready():
    print('ログインしました')


def create_token(n):
    rands = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(rands)


@slash.slash(name='lab', description='KUN Labへ行き、プログラミング勢と会話をすることができます。', guild_ids=[REQUEST_SERVER_ID])
async def on_message(ctx: SlashContext):
    if ctx.channel_id != REQUEST_CHANNEL_ID:
        await ctx.send(f'/lab コマンドは <#{REQUEST_CHANNEL_ID}> チャンネルで使うことができます。')
        return

    id_cells = ws.findall(str(ctx.author_id), in_column=3)
    if not id_cells or ctx.author_id is None:
        await ctx.send(
            embeds=[
                discord.Embed(
                    title='❌ 招待リンク発行失敗',
                    description=
                    f'アカウントの照会に失敗しました。\n'
                    f'かめすたにお問い合わせください。'
                )
            ]
        )
        return

    cell = id_cells[0]
    row = cell.row
    user_id = ws.range(f'A{row}:A{row}')[0].value
    user_token = ws.range(f'B{row}:B{row}')[0].value

    if not user_token:
        user_token = create_token(8)
        ws.update(f'B{row}', user_token)

    ws.update(f'G{row}', datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'), value_input_option="USER_ENTERED")

    await ctx.author.send(
        embed=discord.Embed(
            title='📝 KUN Lab 招待リンク',
            description=
            f'以下の招待リンクからKUN Labへ参加し、認証コードを入力してください。',
            url=INVITE_LINK,
        )
            .add_field(name='ID', value=f'S{user_id}')
            .add_field(name='認証コード', value=user_token)
    )
    await ctx.author.send(INVITE_LINK)

    await ctx.send(
        embeds=[
            discord.Embed(
                title='✅ KUN Lab への招待リンク',
                description=
                f'DMに招待リンクと認証コードを送信しました。\n'
                f'DMをご確認ください。'
            )
        ]
    )


@client.event
async def on_message(message: discord.Message):
    if message.channel.id != USE_CHANNEL_ID:
        return

    author: discord.Member = message.author

    if author.bot:
        return

    if len(message.content) != 8:
        return

    id_cells = ws.findall(str(author.id), in_column=4)
    if id_cells:
        await message.channel.send(
            embed=discord.Embed(
                title='❌登録失敗',
                description=
                'すでに認証済みです'
            )
        )
        return

    token_cells = ws.findall(message.content, in_column=2)
    if not token_cells:
        await message.channel.send(
            embed=discord.Embed(
                title='❌登録失敗',
                description=
                '無効な認証コードです'
            )
        )
        return

    cell = token_cells[0]
    row = cell.row
    user_id = ws.range(f'A{row}:A{row}')[0].value
    user_name = ws.range(f'F{row}:F{row}')[0].value

    discord_cell = ws.range(f'C{row}:D{row}')
    if discord_cell[1].value:
        await message.channel.send(
            embed=discord.Embed(
                title='❌登録失敗',
                description=
                'トークンは使用されています'
            )
        )
        return

    if discord_cell[0].value and discord_cell[0].value != str(author.id):
        await message.channel.send(
            embed=discord.Embed(
                title='❌登録失敗',
                description=
                '不正なユーザーです'
            )
        )
        return

    ws.update(f'C{row}:D{row}', [[str(author.id), str(author)]])

    role = message.guild.get_role(ROLE_ID)
    await author.add_roles(role, reason='認証完了')
    try:
        await author.edit(nick=f'[S{user_id}] {user_name}')
    except discord.errors.Forbidden:
        pass

    await message.channel.send(
        embed=discord.Embed(
            title='✅ 認証完了',
            description=
            f'`{user_name}` さん、認証ありがとうございます。\n'
            f'あなたのIDは `S{user_id}` です'
        )
    )


client.run(os.environ["DISCORD_TOKEN"])
