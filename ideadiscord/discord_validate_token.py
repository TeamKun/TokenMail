import os

import discord
import gspread

from ideadiscord import sheet_constant

# 認証チャンネル
CHANNEL_ID = sheet_constant.discord_channel_id
# ロール
ROLE_ID = sheet_constant.discord_role_id

# Spread Sheet
gc = gspread.oauth()

sh = gc.open_by_key(sheet_constant.sheet_id)
ws = sh.worksheet(sheet_constant.sheet_name)

# Discord
client = discord.Client()


@client.event
async def on_ready():
    print('ログインしました')


@client.event
async def on_message(message: discord.Message):
    if message.channel.id != CHANNEL_ID:
        return

    author: discord.Member = message.author

    if author.bot:
        return

    if len(message.content) != sheet_constant.num_token_length:
        return

    id_cells = ws.findall(str(author.id), in_column=sheet_constant.sheet_column(sheet_constant.column_discord_id))
    if id_cells:
        await message.channel.send(
            embed=discord.Embed(
                title='❌登録失敗',
                description=
                'すでに認証済みです'
            )
        )
        return

    token_cells = ws.findall(message.content, in_column=sheet_constant.sheet_column(sheet_constant.column_token))
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
    user_data = ws.get(f'{sheet_constant.column_number_id}{row}')
    user_id = user_data[0][0]
    user_id_str = format(user_id, '0>3')

    discord_cell_id = ws.range(f'{sheet_constant.column_discord_id}{row}:{sheet_constant.column_discord_id}{row}')
    discord_cell_tag = ws.range(f'{sheet_constant.column_discord_tag}{row}:{sheet_constant.column_discord_tag}{row}')
    if discord_cell_id[0].value or discord_cell_tag[0].value:
        await message.channel.send(
            embed=discord.Embed(
                title='❌登録失敗',
                description=
                'トークンは使用されています'
            )
        )
        return

    ws.batch_update([
        {'range': f'{sheet_constant.column_discord_id}{row}', 'values': [[str(author.id)]]},
        {'range': f'{sheet_constant.column_discord_tag}{row}', 'values': [[str(author)]]},
    ])

    role = message.guild.get_role(ROLE_ID)
    await author.add_roles(role, reason='認証完了')
    # try:
    #     await author.edit(nick=f'[L{user_id_str}] {author.display_name}')
    # except discord.errors.Forbidden:
    #     pass

    await message.channel.send(
        embed=discord.Embed(
            title='✅ 認証完了',
            description=
            f'`{str(author)}` さん、認証ありがとうございます。\n'
            f'あなたのIDは `A{user_id_str}` です'
        )
    )


client.run(os.environ["DISCORD_TOKEN"])
