import json
import os
import random
import logging
import aiohttp
from random import randrange
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get
from discord import Embed
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

bot = commands.Bot(command_prefix=commands.when_mentioned_or(','), help_command=None)

# help command
@bot.command(brief="shows this message", description="shows this message")
async def help(ctx):
    colors = [0x4ef207, 0x6f5df0, 0x40ffcf, 0xa640ff, 0xe00d6c, 0xb2e835]
    color = random.choice(colors)
    embed = discord.Embed(
        title="Kermit's commands", url="https://en.wikipedia.org/wiki/Kermit_the_Frog", color=color
    )
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    for command in bot.commands:
        if (command != say and command != reply and command != speak and command != servers and command != secret and command != edit and command != schedule):
            if (command == clear):
                embed.add_field(name="clear (admins only)", value=command.description, inline=True)
            elif (command == proll):
                embed.add_field(name="proll (number of options)", value=command.description, inline=True)
            else:
                embed.add_field(name=command, value=command.description, inline=True)
    embed.add_field(name="DM feature", value="try to DM me!", inline=True)
    embed.set_thumbnail(url=config['thumbnail_url'])
    embed.set_footer(text=f"Information requested by: {ctx.author.display_name}")
    await ctx.send(embed=embed)

# clear command
@bot.command(brief="clears entered amount of messages", description="clears entered amount of messages")
async def clear(ctx, amount : int):
    _id = ctx.author.id
    mention = mention = f'<@!{366117920960675843}>' # RoastSea8
    if (_id == config['my_id'] or ctx.author.guild_permissions.administrator):
        await ctx.channel.purge(limit = amount + 1)
    else:
        await ctx.send("Sorry, only admins and the creator of Kermit can use this command.")
        return

# text-through command
@bot.command()
async def say(ctx, arg1, *, arg):
    _id = ctx.author.id
    if (_id != config['my_id']):
        await ctx.send("This is a private command!")
        return
    else:
        if (arg1.isnumeric()):
            arg1 = int(arg1)
        else:
            arg1 = config[arg1]
    channel = bot.get_channel(arg1)
    try:
        await channel.send(ctx.message.attachments[0].url)
    except IndexError:
        pass
    await channel.send(arg)

# edit command
@bot.command()
async def edit(ctx, _channel, msg_id : int, *, edited):
    if (ctx.author.id != config['my_id']):
        return
    if (_channel.isnumeric()):
            _channel = int(_channel)
    else:
        _channel = config[_channel]
    channel = bot.get_channel(_channel)
    message = await channel.fetch_message(msg_id)
    await message.edit(content=str(edited))

# speak command
@bot.command()
async def speak(ctx, *, arg):
    _id = ctx.author.id
    if ((_id == config['my_id']) or (_id == config['lyra']) or (_id == config['minsui'])):
        await ctx.send(arg, tts=True)
    else:
        await ctx.send("This is a private command!")
        return

# reply command
@bot.command()
async def reply(ctx, arg1, *, arg):
    _id = ctx.author.id
    if (_id != config['my_id']):
        await ctx.send("This is a private command!")
        return
    else:
        if (arg1.isnumeric()):
            user_id = int(arg1)
        else:
            user_id = config[arg1]
        user = await bot.fetch_user(user_id)
        await user.send(arg)

# poll command
@bot.command(brief="sets up a poll", description="sets up a poll")
async def poll(ctx, *, arg):
    # await ctx.send('{} Poll started by {}: '.format(ctx.message.guild.roles[0], ctx.author.mention))
    await ctx.message.delete()
    await ctx.send('Poll started by {}: '.format(ctx.author.mention))
    m = await ctx.send('`{}`'.format(arg))
    await m.add_reaction('👍')
    await m.add_reaction('👎')
    await m.add_reaction('🤷')

poll_options = ['🇦','🇧','🇨','🇩','🇪','🇫','🇬','🇭','🇮','🇯','🇰',
'🇱','🇲','🇳','🇴','🇵','🇶','🇷','🇸','🇹','🇺','🇻','🇼','🇽','🇾','🇿']

# pro poll command
@bot.command(description="sets up a poll with entered number of options")
async def proll(ctx, args : int, *, content):
    await ctx.message.delete()
    await ctx.send('Poll started by {}: '.format(ctx.author.mention))
    m = await ctx.send('`{}`'.format(content))
    for i in range(args):
        await m.add_reaction(poll_options[i])

# # math command
# @bot.command(brief="does math", description="does math so that your stupid self doesn't have to")
# async def calc(ctx, *, math):
#     await ctx.send(f'{math} = {eval(math)}')
#     if (random.randint(0, 2) == 1):
#         await ctx.send("Imagine not being able to do that 🤡")

# suggests command
@bot.command(brief="sends feature suggestions to Kermit", description="sends feature suggestions to Kermit")
async def suggest(ctx, *, suggestion):
    channel = bot.get_channel(config['suggestions_channel'])
    await channel.send(f'`{(str(ctx.author)[:-5])} suggests`: {suggestion}')
    try:
        await channel.send(ctx.message.attachments[0].url)
    except IndexError:
        pass
    _id = ctx.author.id
    user = await bot.fetch_user(_id)
    await user.send('Your suggestion has been received!')

# troll token command
@bot.command(brief="provides Kermit's token", description="provides Kermit's token")
async def token(ctx):
    await ctx.send("Here's my token: `{}`\nHave fun!".format(config['troll_token']))

# provides invite link
@bot.command(brief='provides link to invite Kermit into a server', description='provides link to invite Kermit into a server')
async def link(ctx):
    app_info = await bot.application_info()
    perms = discord.Permissions.none()
    url = discord.utils.oauth_url(app_info.id, perms)
    await ctx.send('To invite me to a server, use this link\n{}'.format(url))

# provides school schedule pic
@bot.command(description="sends school schedule b/g")
async def schedule(ctx):
    await ctx.send(file=discord.File('images/schedule.png'))

# get names of servers that bot belongs to
@bot.command()
async def servers(ctx):
    if (ctx.author.id != config['my_id']):
        return
    await ctx.send('Servers connected to:')
    for guild in bot.guilds:
        await ctx.send(guild.name)

# prints out all commands with descriptions
@bot.command()
async def commands(ctx):
    if ctx.author.id != config['my_id']:
        return
    for command in bot.commands:
        await ctx.send(f'{command}: {command.description}')

# responding to unknown servers
@bot.command()
async def secret(ctx, guild_name, channel_name, *, message):
    if (ctx.author.id != config['my_id']):
        return
    for guild in bot.guilds:
        guild_name = guild_name.replace('-', ' ')
        if (guild_name == ((str(guild.name).lower()))):
            try:
                channel = get(guild.text_channels, name=channel_name)
            except:
                await ctx.send(f"channel not found in {guild}")
                await ctx.send(channel.name)
                return
            await channel.send(message)

emojis = ['🤡', '😐', '😳', '🧢', '🏳️‍🌈', '💩', '😈', '🤓']
servers = ['BotTestingServer', 'battle bus', 'FW_OUI', 'The New Boys and I', 'Abandoned Musical Train Station', 'my dog is life <3']

@bot.event
async def on_message(message):
    channel = message.channel
    username = message.author.name
    user_id = message.author.id

    if message.author == bot.user:
        return
    
    await bot.process_commands(message)
        
    # emoji = random.choice(emojis)
    # last_emote = emoji
    # if (emoji == last_emote):
    #     emoji = random.choice(emojis)
    # if (randrange(15) == 1):
    #     await message.add_reaction(emoji)
    #     if (randrange(6) == 1):
    #         emoji = random.choice(emojis)
    #         await message.add_reaction(emoji)

    mention = f'<@!{bot.user.id}>'
    if mention in message.content:
        if (random.randint(0,1) == 1):
            await channel.send("https://tenor.com/view/kermit-the-frog-drive-driving-gif-3965525")

    channel = bot.get_channel(config['bot_testing_channel'])
    if message.guild is None and message.author != bot.user:
        await channel.send(f'`{(str(message.author)[:-5])}`: {message.content}')
        try:
            await channel.send(message.attachments[0].url)
        except IndexError:
            pass
    
    _guild = bot.get_guild(config['bot_testing_server'])
    for server in servers:
        if (str(message.guild.name) == server):
            return
    gld_name = (str(message.guild.name)).lower()
    gld_name = gld_name.replace(' ', '-')
    server_channel = get(_guild.text_channels, name=gld_name)
    if server_channel is None:
        return
    embed = discord.Embed(
        title=f'{message.channel}', description=f'{message.content}'
    )
    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
    await server_channel.send(embed=embed)
    try:
        await server_channel.send(message.attachments[0].url)
    except IndexError:
        pass
    embeds = message.embeds
    if not embeds:
        return
    else:
        embed = (message.embeds)[0]
        await server_channel.send(embed=embed)

# missing arguments event
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all required arguments.')
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send('Bot is missing permissions.')

# prints out if bot has been added into another server
@bot.event
async def on_guild_join(guild):
    channel = bot.get_channel(config['server_invites_channel'])
    await channel.send(f'Kermit has been added to: {guild}')

    _guild = bot.get_guild(config['bot_testing_server'])

    category = discord.utils.get(_guild.categories, name="servers")
    gld_name = (str(guild.name)).lower()
    await _guild.create_text_channel(gld_name, category=category)

# loading all cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

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

    # Setting `Playing ` status
    # await bot.change_presence(activity=discord.Game(name="with Elmo"), status=discord.Status.dnd)

    # Setting `Streaming ` status
    # await bot.change_presence(activity=discord.Streaming(name="My Thug Life", url="https://www.youtube.com/watch?v=nsaH7gjZYXE"))

    # Setting `Listening ` status
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=",help"), status=discord.Status.online)

    # Setting `Watching ` status
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"), status=discord.Status.dnd)

if __name__ == '__main__':
    try:
        bot.run(os.environ['token'])
    except KeyError:
        print("config not yet filled out.")
    except discord.errors.LoginFailure as e:
        print("Invalid discord token.")