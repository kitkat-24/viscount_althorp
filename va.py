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


@bot.command(pass_context = True)
async def adduser(ctx, user : discord.User, nation):
    """Add a user to the users table.
    Requires an @mentioned user and their nation (separated by a space)."""
    client = MongoClient(MONGODB_URI)
    # As far as I can tell, on the free plan you're only allowed to access the
    # default database created for you by heroku.
    db = client.get_database()
    users = db['users'] # Select or create collection

    user_data = {'uid' : user.id, 'username' : user.name,
            'discriminator' : user.discriminator, 'nation' : nation}
    users.insert_one(user_data)
    client.close() # Clean up

    await ctx.send('Added {} playing as {}.'.format(user.name, nation))


@bot.command(pass_context = True)
async def addnation(ctx, user : discord.User, nation, pres, ind, mil, pop):
    """Add a nation to the nation collection.

    Requires an @mentioned user, their nation, prestige, industry, and mil
    scores, and the population (separated by spaces, no commas in numbers)."""
    client = MongoClient(MONGODB_URI)
    db = client.get_database()
    nations = db['nations'] # Select or create collection

    n_data = {'nation' : nation, 'uid' : user.id, 'prestige' : pres,
            'industry' : ind, 'military' : mil, 'pop' : pop}
    nations.insert_one(n_data)
    client.close() # Clean up

    await ctx.send('Added {} playing as {}.'.format(user.name, nation))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-'*max(len(bot.user.name), len(str(bot.user.id))))

cogs = ['cogs.userquery', 'cogs.utility']

if __name__ == '__main__':
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(f'Failed to load {cog}.')
            traceback.print_exc()

# Actually run the bot
bot.run(BOT_TOKEN, bot=True, reconnect=True)
