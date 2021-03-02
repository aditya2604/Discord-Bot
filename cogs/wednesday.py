import discord, datetime
from discord.ext import commands, tasks
import json

with open('config.json') as f:
    config = json.load(f)

class wednesday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @tasks.loop(seconds=10)
    async def time_checker(self):
        self.channel = await self.bot.fetch_channel(config['blue'])
        self.time = datetime.datetime.now
        if self.time().hour == 10:
            if datetime.datetime.today().weekday() == 1:
                await self.channel.send(file=discord.File('images/schedule.png'))
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.time_checker.start()

def setup(bot):
    bot.add_cog(wednesday(bot))