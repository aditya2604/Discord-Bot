import discord, datetime
from discord.ext import commands, tasks
import json

with open('config.json') as f:
    config = json.load(f)


class Wednesday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = None
        self.channel_1 = None
        self.channel_2 = None
        self.channel_3 = None
        self.time = datetime.datetime.now
    
    @tasks.loop(hours=1)
    async def time_checker(self):
        self.time = datetime.datetime.now
        if self.time().hour == 12:
            if datetime.datetime.today().weekday() == 2:
                self.channel = await self.bot.fetch_channel(config['g'])
                self.channel_1 = await self.bot.fetch_channel(config['fg'])
                self.channel_2 = await self.bot.fetch_channel(config['ag'])
                self.channel_3 = await self.bot.fetch_channel(config['blue'])
                await self.channel.send(file=discord.File('media/wednesday_pic.png'))
                await self.channel_1.send(file=discord.File('media/wednesday_pic.png'))
                await self.channel_2.send(file=discord.File('media/wednesday_pic.png'))
                await self.channel_3.send(file=discord.File('media/wednesday_pic.png'))
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        print("day: " + str(datetime.datetime.today().weekday()))
        print("hour: " + str(datetime.datetime.now().hour)) 
        self.time_checker.start()


def setup(bot):
    bot.add_cog(Wednesday(bot))
