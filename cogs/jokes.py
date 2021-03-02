import discord
from discord.ext import commands
import pyjokes

class jokes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(brief="tells a joke", description="tells a joke")
    async def joke(self, ctx):
        await ctx.send(pyjokes.get_joke())
    
def setup(bot):
    bot.add_cog(jokes(bot))