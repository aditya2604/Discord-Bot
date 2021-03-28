import discord, datetime
from discord.ext import commands

start_time = datetime.datetime.utcnow()


class Time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.start_time = datetime.datetime.now().time().strftime('%H:%M:%S')

    @commands.command(description="displays the amount of time Kermit has been online for")
    async def uptime(self, ctx):
        current_time = datetime.datetime.now().time().strftime('%H:%M:%S')
        tdelta = str(abs((datetime.datetime.strptime(current_time,'%H:%M:%S') - datetime.datetime.strptime(self.start_time,'%H:%M:%S'))))
        i = tdelta.find(':')
        tdelta = tdelta.replace(':', " hours, ", 1)
        tdelta = tdelta.replace(':', " minutes, ", 1)
        tdelta += " seconds"
        embed = discord.Embed(color=discord.Color.dark_gold())
        embed.add_field(name="uptime", value=tdelta, inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Time(bot))
