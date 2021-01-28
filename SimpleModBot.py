import json
import random
import logging
import aiohttp
from random import randrange
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
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
@bot.command(brief="clears the entered amount of messages", description="clears the entered amount of messages(needs 'manage messages' perms to work")
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit = amount)

# text-through command
@bot.command(brief="private command", description="not accessible to users")
async def say(ctx, arg1, *, arg):
    channel = bot.get_channel(config[arg1])
    await channel.send(arg)

# poll command
@bot.command(brief="sets up a poll", description="sets up a poll")
async def poll(ctx, *, arg):
    # await ctx.send('{} Poll started by {}: '.format(ctx.message.guild.roles[0], ctx.author.mention))
    if (ctx.channel.guild.me.guild_permissions.manage_messages):
        await ctx.channel.purge(limit = 1)
    await ctx.send('Poll started by {}: '.format(ctx.author.mention))
    m = await ctx.send('`{}`'.format(arg))
    await m.add_reaction('👍')
    await m.add_reaction('👎')
    await m.add_reaction('🤷')

# join vc command
@bot.command(brief="joins current voice channel", description="joins current voice channel")
async def join(ctx):
    voice_channel = ctx.author.voice.channel
    await voice_channel.connect()

# leave vc command
@bot.command(brief="leaves current voice channel", description="leaves current voice channel")
async def leave(ctx):
    await ctx.voice_client.disconnect()

# speak command
@bot.command(brief="text to speech", description="speaks out the entered argument")
async def speak(ctx, *, arg):
    if (ctx.author.id != config['my_id']):
        return
    else:
        await ctx.send(arg, tts=True)

emojis = ['🤡', '😐', '😳', '🧢', '🏳️‍🌈', '💩', '😈', '🤓', '👲']

@bot.event
async def on_message(message: discord.Message):
    channel = message.channel
    username = message.author.name
    user_id = message.author.id

    if (user_id == config['bot_id']):
        return
        
    emoji = random.choice(emojis)
    last_emote = emoji
    if (emoji == last_emote):
        emoji = random.choice(emojis)
    if (randrange(10) == 1):
        await message.add_reaction(emoji)
        if (randrange(6) == 1):
            emoji = random.choice(emojis)
            await message.add_reaction(emoji)
    mention = f'<@!{bot.user.id}>'
    if mention in message.content:
        if (random.randint(0,1) == 1):
            await channel.send("https://tenor.com/view/kermit-the-frog-drive-driving-gif-3965525")
    await bot.process_commands(message)

# missing arguments function
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all required arguments.')

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
