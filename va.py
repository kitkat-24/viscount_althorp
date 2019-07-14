import asyncio
import discord # discord.py rewrite
from discord.ext import commands
import os
import traceback
import sys


bot = commands.Bot(command_prefix='.')

cogs = ['cogs.userquery', 'cogs.adminquery', 'cogs.rolls', 'cogs.utility',
        'cogs.test', 'cogs.secret', 'cogs.crunch', 'cogs.embed']


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-' * max(len(bot.user.name), len(str(bot.user.id))))

    # Default help command is over-written in cogs.embed
    #bot.remove_command('help')
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(f'Failed to load {cog}.', file=sys.stderr)
            traceback.print_exc()



if __name__ == '__main__':
    BOT_TOKEN = os.environ['BOT_TOKEN']  # Load bot token from heroku env
    bot.run(BOT_TOKEN, bot=True, reconnect=True)  # Actually run the bot
