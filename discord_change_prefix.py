import discord
import os
import re

# 鯖
GUILD_ID = 792782781674684438

# Discord
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('ログインしました')

    guild: discord.Guild = await client.fetch_guild(GUILD_ID)

    async for member in guild.fetch_members():
        m = re.search('^\\[([KL])(\\d+)\\] (.+)$', member.display_name)
        if m is not None:
            user_type = m.group(1)
            user_id = m.group(2)
            user_name = m.group(3)
            user_id_str = format(user_id, '0>2')
            display_name = f'[{user_type}{user_id_str}] {user_name}'

            if display_name != member.display_name:
                try:
                    await member.edit(nick=display_name)
                except discord.errors.Forbidden:
                    pass

                print(display_name)

    print('完了')
    exit(0)


client.run(os.environ["DISCORD_TOKEN"])
