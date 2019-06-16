import random
import discord
from discord.ext import commands


class UtilityCog(commands.Cog, name="Utility Commands"):
    def __init__(self, bot):
        self.bot = bot

    # ----------cog methods----------#

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *choices: str):
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

    @commands.command()
    async def roll(self, ctx, dice: str, mod: int = 0):
        """Rolls dice in NdN + modifier format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        result = [random.randint(1, limit) for r in range(rolls)]

        # Build strings of roll +/- modifier
        rolls = []
        total = 0
        for r in result:
            # Threshold total so that each die adds between 1 and limit
            inc = r + mod
            if inc < 1:
                total += 1
            elif inc > limit:
                total += limit
            else:
                total += inc

            # Highlight crit successes and failures
            if r == limit:
                r = '***{}***'.format(limit)
            elif r == 1:
                r = '***1***'
            # Print roll and modifier
            if mod > 0:
                rolls.append('{} + {}'.format(r, mod))
            elif mod < 0:
                rolls.append('{} - {}'.format(r, abs(mod)))
            else:
                rolls.append('{}'.format(r))

        await ctx.send('Rolled {}    (sum: {})'.format(', '.join(rolls), total))

    @commands.command()
    async def whoareyou(self, ctx):
        """Describe the bot."""
        wiki_url = 'https://en.wikipedia.org/wiki/John_Spencer,_3rd_Earl_Spencer'
        await ctx.send('I am a bot for computing sums and generally helping facilitate the RP.\n'
                       'Check out my wikipedia page to learn more about me:\n<{}>'.format(wiki_url))


def setup(bot):
    bot.add_cog(UtilityCog(bot))
