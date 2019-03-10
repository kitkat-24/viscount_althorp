import discord # discord.py rewrite
from discord.ext import commands
from discord.utils import get
import os
from pymongo import MongoClient

# Load database URI from heroku env
MONGODB_URI = os.environ['MONGODB_URI']


class UserQueryCog(commands.Cog, name="User Commands"):
    def __init__(self, bot):
        self.bot = bot


    #----------cog methods----------#

    @commands.command(pass_context = True)
    async def checkuser(self, ctx, user : discord.User):
        """Check if a user is in the users table."""
        client = MongoClient(MONGODB_URI)
        db = client.get_database()
        users = db['users'] # Select or create collection

        query = {'uid' : user.id}
        result = users.find_one(query) # Use find_one() since we know id is unique
        if result: # result should be None if not found
            await ctx.send('Found user {}.'.format(user.name))
        else:
            await ctx.send('Could not find user {}.'.format(user.name))

        client.close()

    @commands.command(pass_context = True)
    async def getnation(self, ctx, user : discord.User):
        """Get the nation for the given player."""
        client = MongoClient(MONGODB_URI)
        db = client.get_database()
        nations = db['nations'] # Select or create collection

        query = {'uid' : user.id}
        result = nations.find_one(query) # Use find_one() since we know id is unique
        if result: # result should be None if not found
            await ctx.send('{}\'s nation is {}.'.format(user.name, result['nation']))
        else:
            await ctx.send('Could not find {}\'s nation.'.format(user.name))

        client.close()

    @commands.command(pass_context = True)
    async def getplayer(self, ctx, nation):
        """Get the player for the given nation."""
        client = MongoClient(MONGODB_URI)
        db = client.get_database()
        nations = db['nations'] # Select or create collection

        query = {'nation' : nation}
        result = nations.find_one(query) # Use find_one() since we know id is unique
        if result: # result should be None if not found
            user = get(self.bot.get_all_members(), id=result['uid'])
            if user:
                await ctx.send('{}\'s player is {}.'.format(nation, user.name))
            else:
                await ctx.send('Player for {} not found.'.format(nation))
        else:
            await ctx.send('Could not find nation {}.'.format(nation))

        client.close()

    @commands.command(pass_context = True)
    async def getnationstats(self, ctx, nation):
        """Show the given nation's information."""
        client = MongoClient(MONGODB_URI)
        db = client.get_database()
        nations = db['nations'] # Select or create collection

        query = {'nation' : nation}
        result = nations.find_one(query) # Use find_one() since we know id is unique
        if result: # result should be None if not found
            embed=discord.Embed(title=" ")
            embed.set_author(name=nation)
            embed.add_field(name="Prestige", value=result['prestige'], inline=True)
            embed.add_field(name="Industry", value=result['industry'], inline=True)
            embed.add_field(name="Military", value=result['military'], inline=True)
            embed.add_field(name="Population", value="{:,}".format(int(result['pop'])), inline=True) # Format as comma-separated int
            await ctx.send(embed=embed)
        else:
            await ctx.send('Could not find nation {}.'.format(nation))

        client.close()


def setup(bot):
    bot.add_cog(UserQueryCog(bot))
