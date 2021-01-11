import discord
import os
import gspread


# 鯖
GUILD_ID = 792782781674684438
# ロール
ROLE_ID = 792788707228123187


# Spread Sheet
gc = gspread.oauth()

sh = gc.open_by_key("1QJmehI1eJDcYUAlDVulUe_P-gez_Xd6S5en0jk0A4B0")
ws = sh.worksheet('ユーザー')


# Discord
client = discord.Client()


@client.event
async def on_ready():
    print('ログインしました')

    selectorB = f'B3:B{ws.row_count}'

    sample = ws.range(selectorB)
    sa_count = max([cell.row for cell in sample if cell.value])
    sh_count = sa_count - 2

    selectorO = f'O3:O{sa_count}'
    selectorS = f'S3:S{sa_count}'

    users = ws.batch_get([selectorO, selectorS])

    guild: discord.Guild = await client.fetch_guild(GUILD_ID)
    role = guild.get_role(ROLE_ID)

    for i in range(sh_count):
        if users[1][i] and users[1][i][0]:
            user_discord = users[0][i][0]

            member: discord.Member = await guild.fetch_member(user_discord)
            await member.add_roles(role, reason='二次選考通過')
            print(f'{member.display_name} にロールを付与した')

    print('完了')
    exit(0)


client.run(os.environ["DISCORD_TOKEN"])
