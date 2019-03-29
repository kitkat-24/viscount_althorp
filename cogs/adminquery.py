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
        self.client = MongoClient(MONGODB_URI)
        # As far as I can tell, on the free plan you're only allowed to access the
        # default database created for you by heroku.
        self.db = self.client.get_database()

    def cog_unload(self):
        self.client.close()
        print("AdminQueryCog unload called on shutdown")


    #----------cog methods----------#

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    #@commands.has_role("Admin") # Is another option I think
    async def adduser(ctx, user : discord.User, nation):
        """Add a user to the users table.
        Requires an @mentioned user and their nation (separated by a space)."""
        users = self.db['users'] # Select or create collection
        user_data = {'uid' : user.id, 'username' : user.name,
                'discriminator' : user.discriminator, 'nation' : nation}
        users.insert_one(user_data)

        await ctx.send('Added {} playing as {}.'.format(user.name, nation))

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    #@commands.has_role("Admin") # Is another option I think
    async def removeuser(ctx, user : discord.User, nation):
        """Remove a user from the users table.
        Requires an @mentioned user and their nation (separated by a space)."""
        users = self.db['users']
        users.delete({'uid': user.id}) # Filter functions like a query

        await ctx.send('Added {} playing as {}.'.format(user.name, nation))

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def addnation(self, ctx, user : discord.User, nation : str, pres : int,
            ind : int, mil : int, pop : int):
        """Add a nation to the nation collection.

        Requires an @mentioned user, their nation, prestige, industry, and mil
        scores, and the population (separated by spaces, no commas in numbers)."""
        nations = self.db['nations'] # Select or create collection
        n_data = {'nation': nation, 'uid': user.id, 'prestige': pres,
                'industry': ind, 'military': mil, 'pop': pop}
        nations.insert_one(n_data)

        await ctx.send('Added {} playing as {}.'.format(user.name, nation))

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def removenation(self, ctx, nation : str):
        """Remove a nation from the nation collection. THIS IS PERMANENT."""
        nations = self.db['nations'] # Select or create collection
        nations.delete_one({"nation": nation})

        await ctx.send('Removed nation {}.'.format(nation))

    #---------------------------Adjustments to Stats----------------------------#
    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def adjustprestige(self, ctx, nation : str, pres : int):
        """Change a nation's prestige score."""
        nations = self.db['nations'] # Select or create collection
        nat = nations.find_one({"nation": nation})

        if nat:
            result = nations.update_one({'nation': nation}, {'$inc': {'prestige': pres}})
            await ctx.send('Updated {}\'s prestige to {}.'.format(nation, nat['prestige'] + pres))
        else:
            await ctx.send('Could not find nation "{}".'.format(nation))

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def adjustindustry(self, ctx, nation : str, ind : int):
        """Change a nation's industry score."""
        nations = self.db['nations'] # Select or create collection
        nat = nations.find_one({"nation": nation})

        if nat:
            result = nations.update_one({'nation': nation}, {'$inc': {'industry': ind}})
            await ctx.send('Updated {}\'s industry to {}.'.format(nation, nat['industry'] + ind))
        else:
            await ctx.send('Could not find nation "{}".'.format(nation))

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def adjustmilitary(self, ctx, nation : str, mil : int):
        """Change a nation's military score."""
        nations = self.db['nations'] # Select or create collection
        nat = nations.find_one({"nation": nation})

        if nat:
            result = nations.update_one({'nation': nation}, {'$inc': {'military': mil}})
            await ctx.send('Updated {}\'s military to {}.'.format(nation, nat['military'] + mil))
        else:
            await ctx.send('Could not find nation "{}".'.format(nation))

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def setpop(self, ctx, nation : str, upper : int, middle : int,
            prole : int, peas : int):
        """Set a nation's population.
        Takes a nation and then their upperclass, middleclass, proletarian, and
        peasant populations (separated by spaces, no commas)."""
        nations = self.db['nations'] # Select or create collection
        nat = nations.find_one({"nation": nation})

        if nat:
            nations.update_one(
                {'nation': nation},
                {
                    '$set': {
                        'pop': {
                            'upper': upper,
                            'middle': middle,
                            'proletarian': prole,
                            'peasant': peas
                         }
                    }
                }
            )
            nat = nations.find_one({"nation": nation})
            await ctx.send('Set {}\'s population to {}.'.format(nation, nat['pop']))
        else:
            await ctx.send('Could not find nation "{}".'.format(nation))

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def adjustpop(self, ctx, nation : str, upper : int, middle : int,
            prole : int, peas : int):
        """Change a nation's population."""
        nations = self.db['nations'] # Select or create collection
        nat = nations.find_one({"nation": nation})

        if nat:
            nations.update_one(
                {'nation': nation},
                {
                    '$inc': {
                        'pop.upper': upper,
                        'pop.middle': middle,
                        'pop.proletarian': prole,
                        'pop.peasant': peas
                    }
                }
            )
            nat = nations.find_one({"nation": nation})
            await ctx.send('Set {}\'s population to {}.'.format(nation, nat['pop']))
        else:
            await ctx.send('Could not find nation "{}".'.format(nation))

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def settech(self, ctx, nation : str, mil : int, nav : int, cul : int,
            comm : int, ind):
        """Set a nation's technology."""
        nations = self.db['nations'] # Select or create collection
        nat = nations.find_one({"nation": nation})

        if nat:
            nations.update_one(
                {'nation': nation},
                {
                    '$set': {
                        'tech.military': mil,
                        'tech.navy': nav,
                        'tech.culture': cul,
                        'tech.commerce': comm,
                        'tech.industry': ind
                    }
                }
            )
            await ctx.send('Set {}\'s tech to `[{} | {} | {} | {} | {}]`.'.format(
                    nation, mil, nav, cul, comm, ind))
        else:
            await ctx.send('Could not find nation "{}".'.format(nation))


def setup(bot):
    bot.add_cog(AdminQueryCog(bot))
