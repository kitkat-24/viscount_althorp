import discord # discord.py rewrite
from discord.ext import commands
from discord.utils import get
import os
from pymongo import MongoClient
import numpy as np


# Load database URI from heroku env
MONGODB_URI = os.environ['MONGODB_URI']


class CrunchCog(commands.Cog, name="Calculation Commands"):
    """For running bigger calculations."""
    def __init__(self, bot):
        self.bot = bot
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client.get_database()

    def cog_unload(self):
        self.client.close()
        print("CrunchCog unload called on shutdown")

    """----------cog methods----------"""

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def manualpop(self, ctx, upper: int, middle: int, military: int,
            proletariat: int, peasant: int, growth_rate: float = 0.0125,
            modifier: float = 1.0):
        """Manually calculate new pops."""
        pop = [upper, middle, military, proletariat, peasant]
        pop = [x ** (1 + modifier*growth_rate) for x in pop]
        s = """After five years: Upper = {0}, Middle = {1}, Military = {2},
               Proletariat = {3}, Peasant = {4}."""

        await ctx.send(s.format(*pop))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def autopop(self, ctx, name: str, growth_rate: float = 0.0125, modifier: float = 1.0):
        """Automatically calculate new pops."""
        nations = self.db['nations']
        nat = nations.find_one({'name': name})

        if nat:
            pop = [nat['pop']['upper'], nat['pop']['middle'], nat['pop']['military'],
                   nat['pop']['proletariat'], nat['pop']['peasant']]
            pop = [x ** (1 + modifier*growth_rate) for x in pop]

            nations.update_one(
                {'name': name},
                {
                    '$set': {
                        'pop': {
                            'upper': pop[0],
                            'middle': pop[1],
                            'military': pop[2],
                            'proletariat': pop[3],
                            'peasant': pop[4]
                        }
                    }
                }
            )
            old_pop = nat['pop']
            nat = nations.find_one({'name': name})
            new_pop = nat['pop']
            await ctx.send('{}\'s population grew from {} to {}.'.format(name, old_pop, new_pop))
        else:
            await ctx.send('Could not find nation "{}".'.format(name))


def setup(bot):
    bot.add_cog(CrunchCog(bot))
