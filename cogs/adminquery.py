import discord # discord.py rewrite
from discord.ext import commands
from discord.utils import get
import os
from pymongo import MongoClient
import numpy as np

# Load database URI from heroku env
MONGODB_URI = os.environ['MONGODB_URI']


class AdminQueryCog(commands.Cog, name="Admin-only Commands"):
    def __init__(self, bot):
        self.bot = bot


    #----------cog methods----------#

    @commands.command()
    @commands.has_permissions(administrator=True)
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
    @commands.has_permissions(administrator=True)
    #@commands.has_role("Admin") # Is another option I think
    async def removeuser(ctx, user : discord.User, nation):
        """Remove a user from the users table.
        Requires an @mentioned user and their nation (separated by a space)."""
        client = MongoClient(MONGODB_URI)
        db = client.get_database()
        users = db['users']

        users.delete({'uid': user.id}) # Filter functions like a query
        client.close() # Clean up

        await ctx.send('Added {} playing as {}.'.format(user.name, nation))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addnation(self, ctx, user : discord.User, nation : str, pres : int,
            ind : int, mil : int, pop):
        """Add a nation to the nation collection.

        Requires an @mentioned user, their nation, prestige, industry, and mil
        scores, and the population (separated by spaces, no commas in numbers)."""
        client = MongoClient(MONGODB_URI)
        db = client.get_database()
        nations = db['nations'] # Select or create collection

        n_data = {'nation': nation, 'uid': user.id, 'prestige': pres,
                'industry': ind, 'military': mil, 'pop': pop}
        nations.insert_one(n_data)
        client.close() # Clean up

        await ctx.send('Added {} playing as {}.'.format(user.name, nation))

    #---------------------------Adjustments to Stats----------------------------#
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def adjustprestige(self, ctx, nation : str, pres : int):
        """Change a nation's prestige."""
        client = MongoClient(MONGODB_URI)
        db = client.get_database()
        nations = db['nations'] # Select or create collection

        nat = nations.find_one({"nation": nation})
        updoot = int(nat["prestige"]) + pres
        result = nations.update_one({'nation': nation}, {'$set': {'prestige': updoot}})
        nat = nations.find_one({'nation': nation})
        client.close() # Clean up

        if result.modified_count == 1:
            await ctx.send('Updated {}\'s prestige to {}.'.format(nation, nat['prestige']))
        else:
            await ctx.send('Could not find nation "{}".'.format(nation))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def adjustindustry(self, ctx, nation : str, ind : int):
        """Change a nation's industry."""
        client = MongoClient(MONGODB_URI)
        db = client.get_database()
        nations = db['nations'] # Select or create collection

        nat = nations.find_one({"nation": nation})
        updoot = int(nat["industry"]) + pres
        result = nations.update_one({'nation': nation}, {'$set': {'industry': updoot}})
        nat = nations.find_one({'nation': nation})
        client.close() # Clean up

        if result.modified_count == 1:
            await ctx.send('Updated {}\'s industry to {}.'.format(nation, nat['industry']))
        else:
            await ctx.send('Could not find nation "{}".'.format(nation))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def adjustmilitary(self, ctx, nation : str, mil : int):
        """Change a nation's military."""
        client = MongoClient(MONGODB_URI)
        db = client.get_database()
        nations = db['nations'] # Select or create collection

        nat = nations.find_one({"nation": nation})
        updoot = int(nat["military"]) + pres
        result = nations.update_one({'nation': nation}, {'$set': {'military': updoot}})
        nat = nations.find_one({'nation': nation})
        client.close() # Clean up

        if result.modified_count == 1:
            await ctx.send('Updated {}\'s military to {}.'.format(nation, nat['military']))
        else:
            await ctx.send('Could not find nation "{}".'.format(nation))


def setup(bot):
    bot.add_cog(AdminQueryCog(bot))
