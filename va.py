import asyncio
import discord # discord.py rewrite
from discord.ext import commands
import os
import random
import traceback, sys



bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-'*max(len(bot.user.name), len(str(bot.user.id))))


cogs = ['cogs.userquery', 'cogs.adminquery', 'cogs.rolls', 'cogs.utility',
        'cogs.test']

if __name__ == '__main__':
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(f'Failed to load {cog}.', file=sys.stderr)
            traceback.print_exc()


BOT_TOKEN = os.environ['BOT_TOKEN'] # Load bot token from heroku env
bot.run(BOT_TOKEN, bot=True, reconnect=True) # Actually run the bot
