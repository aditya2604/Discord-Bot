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
                try:
                    self.channel = await self.bot.fetch_channel(config['g'])
                    await self.channel.send(file=discord.File('media/wednesday_pic.png'))
                except:
                    pass

                try:
                    self.channel = await self.bot.fetch_channel(config['fg'])
                    await self.channel.send(file=discord.File('media/wednesday_pic.png'))
                except:
                    pass

                try:
                    self.channel = await self.bot.fetch_channel(config['ag'])
                    await self.channel.send(file=discord.File('media/wednesday_pic.png'))
                except:
                    pass

                try:
                    self.channel = await self.bot.fetch_channel(config['dg'])
                    await self.channel.send(file=discord.File('media/wednesday_pic.png'))
                except:
                    pass

                try:
                    self.channel = await self.bot.fetch_channel(config['blue'])
                    await self.channel.send(file=discord.File('media/wednesday_pic.png'))
                except:
                    pass
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        print("day: " + str(datetime.datetime.today().weekday()))
        print("hour: " + str(datetime.datetime.now().hour)) 
        self.time_checker.start()


def setup(bot):
    bot.add_cog(Wednesday(bot))
