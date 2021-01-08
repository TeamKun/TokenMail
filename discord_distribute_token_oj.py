import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash import SlashContext
import os
import gspread
import datetime

# 認証チャンネル
CHANNEL_ID = 796924165721423892

# Spread Sheet
gc = gspread.oauth()

sh = gc.open_by_key('1QJmehI1eJDcYUAlDVulUe_P-gez_Xd6S5en0jk0A4B0')
ws = sh.worksheet('ユーザー')

# Discord
client = discord.Client()
slash = SlashCommand(client, auto_register=True)


@client.event
async def on_ready():
    print('ログインしました')


@slash.slash(name='account', description='Webテスト用のIDを発行します', guild_ids=[792782781674684438])
async def on_message(ctx: SlashContext):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send(4, '/account コマンドは <#796924165721423892> チャンネルで使うことができます。')
        return

    user: discord.User = await client.fetch_user(ctx.author)

    id_cells = ws.findall(str(ctx.author), in_column=15)
    if not id_cells or user is None:
        await ctx.send(
            embeds=[
                discord.Embed(
                    title='❌ ID発行失敗',
                    description=
                    f'アカウントの照会に失敗しました。\n'
                    f'かめすたにお問い合わせください。'
                )
            ]
        )
        return

    cell = id_cells[0]
    row = cell.row
    user_data = ws.batch_get([f'Q{row}', f'M{row}'])
    user_id = user_data[1][0][0]
    user_token = user_data[0][0][0]

    ws.update(f'R{row}', datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'), value_input_option="USER_ENTERED")

    await user.send(
        embed=discord.Embed(
            title='📝 KUN Lab Webテスト',
            description=
            f'下記のアカウントでログインし、Webテストを受験してください。',
            url='https://exam.lab.kunmc.net/contest/2',
        )
            .add_field(name='ID', value=f'K{user_id}')
            .add_field(name='パスワード', value=user_token)
    )

    await ctx.send(
        embeds=[
            discord.Embed(
                title='✅ ID発行完了',
                description=
                f'DMにIDとパスワードを送信しました。\n'
                f'DMをご確認ください。'
            )
        ]
    )


client.run(os.environ['DISCORD_TOKEN'])
