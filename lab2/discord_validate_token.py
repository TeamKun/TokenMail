import discord
import os
import gspread


# 認証チャンネル
CHANNEL_ID = 792794338336964620
# ロール
ROLE_ID = 792792490842783762


# Spread Sheet
gc = gspread.oauth()

sh = gc.open_by_key("1QJmehI1eJDcYUAlDVulUe_P-gez_Xd6S5en0jk0A4B0")
ws = sh.worksheet('第2回通過者')


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

    if len(message.content) != 7:
        return

    id_cells = ws.findall(str(author.id), in_column=16)
    if id_cells:
        await message.channel.send(
            embed=discord.Embed(
                title='❌登録失敗',
                description=
                'すでに認証済みです'
            )
        )
        return

    token_cells = ws.findall(message.content, in_column=17)
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
    user_data = ws.batch_get([f'O{row}', f'P{row}'])
    user_id = user_data[1][0][0]
    user_name = user_data[0][0][0]
    user_id_str = format(user_id, '0>2')

    discord_cell = ws.range(f'R{row}:S{row}')
    if discord_cell[0].value or discord_cell[1].value:
        await message.channel.send(
            embed=discord.Embed(
                title='❌登録失敗',
                description=
                'トークンは使用されています'
            )
        )
        return

    ws.update(f'R{row}:S{row}', [[str(author.id), str(author)]])

    role = message.guild.get_role(ROLE_ID)
    await author.add_roles(role, reason='認証完了')
    try:
        await author.edit(nick=f'[L{user_id_str}] {author.display_name}')
    except discord.errors.Forbidden:
        pass

    await message.channel.send(
        embed=discord.Embed(
            title='✅ 認証完了',
            description=
            f'`{user_name}` さん、認証ありがとうございます。\n'
            f'あなたのIDは `L{user_id_str}` です'
        )
    )


client.run(os.environ["DISCORD_TOKEN"])
