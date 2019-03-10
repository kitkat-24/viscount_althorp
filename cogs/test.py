import random
import discord
from discord.ext import commands


class TestCog(commands.Cog, name="Test Commands"):
    def __init__(self, bot):
        self.bot = bot


    #----------cog methods----------#

    @commands.command(hidden=True)
    async def inttype(self, ctx, num : int):
        """Check parameter typecasting"""
        await ctx.send(type(num))

    @commands.command(hidden=True)
    async def listarg(self, ctx, l : List[int]):
        """Try to parse a list of integers."""
        awaitctx.send("L: {}, type: {}".format(str(l), type(l)))




def setup(bot):
    bot.add_cog(TestCog(bot))

