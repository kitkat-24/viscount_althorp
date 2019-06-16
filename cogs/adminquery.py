import discord  # discord.py rewrite
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

    """----------cog methods----------"""

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    # @commands.has_role("Admin") # Is another option I think
    async def adduser(self, ctx, user: discord.User, nation: str):
        """Add a user to the users table.
        Requires an @mentioned user and their nation (separated by a space)."""
        users = self.db['users']  # Select or create collection
        user_data = {'uid': user.id, 'username': user.name,
                     'discriminator': user.discriminator, 'nation': nation}
        users.insert_one(user_data)

        await ctx.send('Added {} playing as {}.'.format(user.name, nation))

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    # @commands.has_role("Admin") # Is another option I think
    async def removeuser(self, ctx, user: discord.User, nation: str):
        """Remove a user from the users table.
        Requires an @mentioned user and their nation (separated by a space)."""
        users = self.db['users']
        users.delete({'uid': user.id})  # Filter functions like a query

        await ctx.send('Added {} playing as {}.'.format(user.name, nation))

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def addnation(self, ctx, user: discord.User, name: str, pres: int,
                        ind: int, mil: int):
        """Add a nation to the nation collection.

        Requires an @mentioned user, their nation, prestige, industry, and mil
        scores (separated by spaces, no commas in numbers)."""
        nations = self.db['nations']  # Select or create collection
        n_data = {'name': name, 'uid': user.id, 'prestige': pres,
                  'industry': ind, 'military': mil}
        nations.insert_one(n_data)

        await ctx.send('Added {} playing as {}.'.format(user.name, name))

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def removenation(self, ctx, name: str):
        """Remove a nation from the nation collection. THIS IS PERMANENT."""
        nations = self.db['nations']  # Select or create collection
        nations.delete_one({'name': name})

        await ctx.send('Removed nation {}.'.format(name))

    # ---------------------------Adjustments to Stats----------------------------#
    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def adjustprestige(self, ctx, name: str, pres: int):
        """Change a nation's prestige score."""
        nations = self.db['nations']  # Select or create collection
        nat = nations.find_one({"nation": name})

        if nat:
            nations.update_one({'name': name}, {'$inc': {'prestige': pres}})
            await ctx.send('Updated {}\'s prestige to {}.'.format(name, nat['prestige'] + pres))
        else:
            await ctx.send('Could not find nation "{}".'.format(name))

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def adjustindustry(self, ctx, name: str, ind: int):
        """Change a nation's industry score."""
        nations = self.db['nations']  # Select or create collection
        nat = nations.find_one({'name': name})

        if nat:
            nations.update_one({'name': name}, {'$inc': {'industry': ind}})
            await ctx.send('Updated {}\'s industry to {}.'.format(name, nat['industry'] + ind))
        else:
            await ctx.send('Could not find nation "{}".'.format(name))

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def adjustmilitary(self, ctx, name: str, mil: int):
        """Change a nation's military score."""
        nations = self.db['nations']  # Select or create collection
        nat = nations.find_one({'name': name})

        if nat:
            nations.update_one({'name': name}, {'$inc': {'military': mil}})
            await ctx.send('Updated {}\'s military to {}.'.format(name, nat['military'] + mil))
        else:
            await ctx.send('Could not find nation "{}".'.format(name))

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def setwestern(self, ctx, name: str, is_western: bool):
        """Set a nation as western or not."""
        nations = self.db['nations']  # Select or create collection
        nat = nations.find_one({'name': name})

        if nat:
            nations.update_one({'name': name}, {'$set': {'western': is_western}})
            if is_western:
                await ctx.send('Set {} to western.'.format(name))
            else:
                await ctx.send('Set {} to non-western.'.format(name))
        else:
            await ctx.send('Could not find nation "{}".'.format(name))

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def setgp(self, ctx, name: str, is_gp: bool):
        """Set a nation as western or not."""
        nations = self.db['nations']  # Select or create collection
        nat = nations.find_one({'name': name})

        if nat:
            nations.update_one({'name': name}, {'$set': {'gp': is_gp}})
            if is_gp:
                await ctx.send('Set {} to great power.'.format(name))
            else:
                await ctx.send('Set {} to non-great power.'.format(name))
        else:
            await ctx.send('Could not find nation "{}".'.format(name))

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def setpop(self, ctx, name: str, upper: int, middle: int, military: int, peas: int):
        """Set a nation's population.
        Takes a nation and then their upperclass, middleclass, military, and
        peasant populations (separated by spaces, no commas)."""
        nations = self.db['nations']  # Select or create collection
        nat = nations.find_one({'name': name})

        if nat:
            nations.update_one(
                {'name': name},
                {
                    '$set': {
                        'pop': {
                            'upper': upper,
                            'middle': middle,
                            'military': military,
                            'peasant': peas
                        }
                    }
                }
            )
            nat = nations.find_one({'name': name})
            await ctx.send('Set {}\'s population to {}.'.format(name, nat['pop']))
        else:
            await ctx.send('Could not find nation "{}".'.format(name))

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def adjustpop(self, ctx, name: str, upper: int, middle: int, military: int, peas: int):
        """Change a nation's population."""
        nations = self.db['nations']  # Select or create collection
        nat = nations.find_one({'name': name})

        if nat:
            nations.update_one(
                {'name': name},
                {
                    '$inc': {
                        'pop.upper': upper,
                        'pop.middle': middle,
                        'pop.military': military,
                        'pop.peasant': peas
                    }
                }
            )
            nat = nations.find_one({"nation": name})
            await ctx.send('Set {}\'s population to {}.'.format(name, nat['pop']))
        else:
            await ctx.send('Could not find nation "{}".'.format(name))

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def settech(self, ctx, name: str, mil: int, nav: int, cul: int, comm: int, ind):
        """Set a nation's technology."""
        nations = self.db['nations']  # Select or create collection
        nat = nations.find_one({'name': name})

        if nat:
            nations.update_one(
                {'name': name},
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
                name, mil, nav, cul, comm, ind))
        else:
            await ctx.send('Could not find nation "{}".'.format(name))


def setup(bot):
    bot.add_cog(AdminQueryCog(bot))
