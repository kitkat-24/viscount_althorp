import random
import numpy as np
import discord
from discord.ext import commands


class Rolls(commands.Cog, name="Stat Commands"):
    def __init__(self, bot):
        self.bot = bot


    #----------cog methods----------#

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def justify(self, ctx, dur : int, maxinf : int):
        """Returns infamy gained due to war goal justification."""
        days = np.random.normal(dur/2, dur*0.375)
        inf = round(maxinf*(days/dur))

        if inf > 0:
            await ctx.send('Discovered! Infamy accrued: {}'.format(inf))
        else:
            await ctx.send('Fabrication not discovered.')


def setup(bot):
    bot.add_cog(Rolls(bot))
