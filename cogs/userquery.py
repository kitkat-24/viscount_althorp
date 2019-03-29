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
        self.client = MongoClient(MONGODB_URI)
        # As far as I can tell, on the free plan you're only allowed to access the
        # default database created for you by heroku.
        self.db = self.client.get_database()

    def cog_unload(self):
        self.client.close()
        print("UserQueryCog unload called on shutdown")


    #----------cog methods----------#

    @commands.command()
    async def checkuser(self, ctx, user : discord.User):
        """Check if a user is in the users table."""
        users = self.db['users'] # Select or create collection
        query = {'uid' : user.id}
        result = users.find_one(query) # Use find_one() since we know id is unique

        if result: # result should be None if not found
            await ctx.send('Found user {}.'.format(user.name))
        else:
            await ctx.send('Could not find user {}.'.format(user.name))

    @commands.command()
    async def getnation(self, ctx, user : discord.User):
        """Get the nation for the given player."""
        nations = self.db['nations'] # Select or create collection
        query = {'uid' : user.id}
        result = nations.find_one(query) # Use find_one() since we know id is unique

        if result: # result should be None if not found
            await ctx.send('{}\'s nation is {}.'.format(user.name, result['nation']))
        else:
            await ctx.send('Could not find {}\'s nation.'.format(user.name))

    @commands.command()
    async def getplayer(self, ctx, nation):
        """Get the player for the given nation."""
        nations = self.db['nations'] # Select or create collection
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

    @commands.command()
    async def getnationstats(self, ctx, nation):
        """Show the given nation's information."""
        nations = self.db['nations'] # Select or create collection
        query = {'nation' : nation}
        result = nations.find_one(query) # Use find_one() since we know id is unique

        if result: # result should be None if not found
            embed=discord.Embed(title=" ")
            embed.set_author(name=nation)
            embed.add_field(name="Prestige", value=result['prestige'], inline=True)
            embed.add_field(name="Industry", value=result['industry'], inline=True)
            embed.add_field(name="Military", value=result['military'], inline=True)
            embed.add_field(name="Upperclass pop", value="{:,}".format(int(result['pop']['upper'])), inline=True) # Format as comma-separated int
            embed.add_field(name="Middleclass pop", value="{:,}".format(int(result['pop']['middle'])), inline=True)
            embed.add_field(name="Proletarian pop", value="{:,}".format(int(result['pop']['proletarian'])), inline=True)
            embed.add_field(name="Peasant pop", value="{:,}".format(int(result['pop']['peasant'])), inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Could not find nation {}.'.format(nation))

    @commands.command()
    async def listnations(self, ctx):
        """List all tracked nations and their players."""
        nations = self.db['nations']

        await ctx.send('__Nation: Player (nickname)__')
        for nation in nations.find():
            user = get(self.bot.get_all_members(), id=nation['uid'])
            if user:
                await ctx.send('{}: {} ({})'.format(nation['nation'], user.name, user.display_name))
            else:
                await ctx.send('{}: Player not found.'.format(nation))


def setup(bot):
    bot.add_cog(UserQueryCog(bot))
