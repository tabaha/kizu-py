
import discord
import asyncio
import json

import pixiv



config = json.load(open('config.json'))
discord_token = config["discord_token"]
pixiv_PHPSESSID = config["pixiv_PHPSESSID"]

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!pixiv'):
        await pixiv.pixivshit(client, message, pixiv_PHPSESSID)

client.run(discord_token)
