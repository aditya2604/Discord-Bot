import json
import random
from datetime import datetime
from discord.ext import commands
try:
    import discord
except ImportError:
    import pip
    pip.main(['install', 'discord'])
    import discord

try:
    with open('config.json') as f:
        config = json.load(f)
except FileNotFoundError:
    with open('config.json', 'w') as f:
        config = {}
        print("config file created.")
        json.dump({'discord_token': '', 'response': '', 'words': ['']}, f)

desc = """
Simple moderation bot.
"""

bot = commands.Bot(command_prefix=',')

# clear command
@bot.command()
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit = amount)

# text-through command
@bot.command()
async def say(ctx, arg1, *, arg):
    channel = bot.get_channel(config[arg1])
    await channel.send(arg)

@bot.event
async def on_message(message: discord.Message):
    channel = message.channel
    username = message.author.name
    user_id = message.author.id

    if (user_id == config['bot_id'] or user_id == config['ayush_id'] or user_id == config['nitish_id'] or user_id == config['pranav_id'] or user_id == config['sid_id'] or user_id == config['steve_id'] or user_id == config['utkarsh_id']):
        return

    await bot.process_commands(message)

@bot.event
async def on_ready():
    app_info = await bot.application_info()
    bot.owner = app_info.owner
    print('Bot: {0.name}:{0.id}'.format(bot.user))
    print('Owner: {0.name}:{0.id}'.format(bot.owner))
    print('------------------')
    perms = discord.Permissions.none()
    perms.administrator = True
    url = discord.utils.oauth_url(app_info.id, perms)
    print('To invite me to a server, use this link\n{}'.format(url))

    #GAMEactivity
    # game = discord.Game(name="wit joe mum", state="In Game")
    # await bot.change_presence(activity=game, status=discord.Status.dnd)

    #STREAMactivity
    # stream = discord.Streaming(platform="YouTube", name="My Drip - Dixie D'Amelio", url="https://youtu.be/k6Kysmn0AO4", details="My Drip - Dixie D'Amelio") 
    # await bot.change_presence(activity=stream, status=discord.Status.idle)

    #WATCHactivity
    #watch = discord.Activity(type=discord.ActivityType.watching, name="video")
    #await client.change_presence(activity=watch, status=discord.Status.idle)

    #LISTENINGactivity
    listen = discord.Activity(type=discord.ActivityType.listening, name="My Drip - Dixie D'Amelio")
    await bot.change_presence(activity=listen, status=discord.Status.online)

if __name__ == '__main__':
    try:
        bot.run(config['discord_token'])
    except KeyError:
        print("config not yet filled out.")
    except discord.errors.LoginFailure as e:
        print("Invalid discord token.")
