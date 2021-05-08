import os
import pandas

import discord

# Discord
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('ログインしました')

    df = pandas.read_csv('users.csv')
    guild: discord.guild.Guild = client.get_guild(827914093116653578)
    srcs = []
    for i in df['ディスコID']:
        member = guild.get_member_named(i)
        srcs.append(member.id if member is not None else 0)

    df['ID'] = srcs
    print(df)
    df.to_csv('ids.csv')


client.run(os.environ["DISCORD_TOKEN"])
