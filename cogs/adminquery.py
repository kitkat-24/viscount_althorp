import discord # discord.py rewrite
from discord.ext import commands
from discord.utils import get
import os
from pymongo import MongoClient
import numpy as np

# Load database URI from heroku env
MONGODB_URI = os.environ['MONGODB_URI']


class AdminQueryCog(commands.Cog, name="Uses Query Commands", hidden=True):
    def __init__(self, bot):
        self.bot = bot


    #----------cog methods----------#

    @commands.command()
    @commands.has_permissions(administrator)
    #@commands.has_role("Admin") # Is another option I think
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

    @commands.command()
    @commands.has_permissions(administrator)
    async def addnation(ctx, user : discord.User, nation : str, pres : int,
            ind : int, mil : int, pop):
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


def setup(bot):
    bot.add_cog(AdminQueryCog(bot))
