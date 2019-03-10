import random
import discord
from discord.ext import commands


class UtilityCog(commands.Cog, name="Utility Commands"):
    def __init__(self, bot):
        self.bot = bot


    #----------cog methods----------#

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *choices : str):
        """Chooses between multiple choices split by commas."""
        temp = " ".join(choices)
        await ctx.send(random.choice(temp.split(',')))

    @commands.command()
    async def hello(self, ctx):
        """Says hello back."""
        await ctx.send(random.choice(['Salutations', 'Greetings', 'Hello there']))

    @commands.command()
    async def pingme(self, ctx):
        """Ping the user who used this command."""
        await ctx.send('{} gotcha'.format(ctx.author.mention))

    # TODO add modifiers to rolls
    @commands.command()
    async def roll(self, ctx, dice : str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        result = [random.randint(1, limit) for r in range(rolls)]
        if rolls > 1:
            await ctx.send('({})    (sum: {})'.format(', '.join(str(n) for n in result), sum(result)))
        else:
            await ctx.send('{}'.format(str(result[0])))

    @commands.command()
    async def whoareyou(self, ctx):
        """Describe the bot."""
        wiki_url='https://en.wikipedia.org/wiki/John_Spencer,_3rd_Earl_Spencer'
        await ctx.send('I am a bot for computing sums and generally helping facilitate the RP.\n' \
                'Check out my wikipedia page to learn more about me:\n<{}>'.format(wiki_url))




def setup(bot):
    bot.add_cog(UtilityCog(bot))
