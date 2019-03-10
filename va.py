#import asyncio
import discord # discord.py rewrite
from discord.ext import commands
import os
from pymongo import MongoClient
import random
import traceback


# Load secure environment variables
BOT_TOKEN = os.environ['BOT_TOKEN']
#SERVER_ID = os.environ['SERVER_ID']


bot = commands.Bot(command_prefix='.')



@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-'*max(len(bot.user.name), len(str(bot.user.id))))

cogs = ['cogs.userquery', 'cogs.adminquery', 'cogs.utility']

if __name__ == '__main__':
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(f'Failed to load {cog}.')
            traceback.print_exc()

# Actually run the bot
bot.run(BOT_TOKEN, bot=True, reconnect=True)
