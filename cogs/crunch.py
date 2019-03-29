import discord # discord.py rewrite
from discord.ext import commands
from discord.utils import get
import os
from pymongo import MongoClient
import numpy as np


# Load database URI from heroku env
MONGODB_URI = os.environ['MONGODB_URI']

"""For running bigger calculations."""
class CrunchCog(commands.Cog, name="Calculation Commands"):
    def __init__(self, bot):
        self.bot = bot
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client.get_database()

    def cog_unload(self):
        self.client.close()
        print("CrunchCog unload called on shutdown")


    #----------cog methods----------#

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def autotick(ctx, user : discord.User, on : bool):
        """Turn automatic year ticks on or off."""
        meta = self.db['meta'] # Select or create collection

        yeartick = meta.find_one({'name': 'yeartick'})
        if on:
            meta.update_one({'name': 'yeartick'}, {'$set': {'on': True}})
            await ctx.send('Turned daily year autotick on.')
        else:
            meta.update_one({'name': 'yeartick'}, {'$set': {'on': False}})
            await ctx.send('Turned daily year autotick off.')

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def getautotick(ctx, user : discord.User):
        """Return year autotick on/off status."""
        meta = self.db['meta']

        yeartick = meta.find_one({'name': 'yeartick'})
        if yeartick['on']:
            await ctx.send('Daily year autotick is on.')
        else:
            await ctx.send('Daily year autotick is off.')

    async def tick():
        """Do the actual math of a yearly tick."""



def setup(bot):
    bot.add_cog(CrunchCog(bot))
