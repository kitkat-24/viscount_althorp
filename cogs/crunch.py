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

    # @commands.command(hidden=True)
    # @commands.has_permissions(administrator=True)
    # async def autotick(self, ctx, on: bool):
    #     """Turn automatic year ticks on or off."""
    #     meta = self.db['meta'] # Select or create collection
    #
    #     yeartick = meta.find_one({'name': 'yeartick'})
    #     if on:
    #         meta.update_one({'name': 'yeartick'}, {'$set': {'on': True}})
    #         await ctx.send('Turned daily year autotick on.')
    #     else:
    #         meta.update_one({'name': 'yeartick'}, {'$set': {'on': False}})
    #         await ctx.send('Turned daily year autotick off.')

    # @commands.command(hidden=True)
    # @commands.has_permissions(administrator=True)
    # async def getautotick(ctx, user : discord.User):
    #     """Return year autotick on/off status."""
    #     meta = self.db['meta']
    #
    #     yeartick = meta.find_one({'name': 'yeartick'})
    #     if yeartick['on']:
    #         await ctx.send('Daily year autotick is on.')
    #     else:
    #         await ctx.send('Daily year autotick is off.')
    #
    # async def tick():
    #     """Do the actual math of a yearly tick."""

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def manualpop(self, ctx, upper: int, middle: int, military: int, lower: int,
                        is_western: bool = True, growth_rate: float = 0.0125, modifier: float = 1.0):
        """Manually calculate new pops."""
        pop = [upper, middle, military, lower]
        for i in range(len(pop)):
            pop[i] = round(pop[i] ** (1 + modifier*growth_rate))
        if is_western:
            lower_to_mid = round((pop[3] - lower) * 0.1)
            pop[1] += lower_to_mid
            pop[3] -= lower_to_mid

        s = 'After five years: Upper = {0}, Middle = {1}, Military = {2}, Lower = {3}.'
        await ctx.send(s.format(*pop))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def autopop(self, ctx, name: str, growth_rate: float = 0.0125, modifier: float = 1.0):
        """Automatically calculate new pops."""
        nations = self.db['nations']
        nat = nations.find_one({"nation": name})

        if nat:
            pop = [nat['pop']['upper'], nat['pop']['middle'], nat['pop']['military'], nat['pop']['peasant']]
            for i in range(len(pop)):
                pop[i] = round(pop[i] ** (1 + modifier * growth_rate))
            if nat['western']:
                lower_to_mid = round((pop[3] - nat['pop']['peasant']) * 0.1)
                pop[1] += lower_to_mid
                pop[3] -= lower_to_mid

            nations.update_one(
                {'nation': name},
                {
                    '$set': {
                        'pop': {
                            'upper': pop[0],
                            'middle': pop[1],
                            'military': pop[2],
                            'peasant': pop[3]
                        }
                    }
                }
            )
            old_pop = nat['pop']
            nat = nations.find_one({"nation": name})
            new_pop = nat['pop']
            await ctx.send('{}\'s population grew from {} to {}.'.format(name, old_pop, new_pop))
        else:
            await ctx.send('Could not find nation "{}".'.format(name))




def setup(bot):
    bot.add_cog(CrunchCog(bot))
