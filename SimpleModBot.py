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
@bot.command()
async def say(ctx, arg1, *, arg):
    channel = bot.get_channel(config[arg1])
    await channel.send(arg)

@bot.event
async def on_message(message: discord.Message):
    channel = message.channel
    username = message.author.name
    user_id = message.author.id

    if (username == "Blueface" or user_id == config['ayush_id'] or user_id == config['nitish_id'] or user_id == config['pranav_id'] or user_id == config['sid_id'] or user_id == config['steve_id'] or user_id == config['utkarsh_id']):
        return

    if any([username in config['usernames']]):
        if (random.randint(1, 2) == 1):
            await channel.send('{} {}{}'.format("I am superior to", username, "."))
            return
        else:
            if (random.randint(1, 2) == 1):
                await channel.send('{} {}{}'.format("I will take", username, "\'s toes and put 'em in my toe jar."))
                return
            else:
                await channel.send('{} {}'.format(message.author.mention, "is stoopid."))
                return

    if any([word in message.content.casefold() for word in config['words2']]):
        if (random.randint(1, 2) == 1):
            await channel.send('{} {}'.format(message.author.mention, config['response2']))
            return
        else:
            await channel.send('{} {}'.format(message.author.mention, config['response2.5']))
            return

    if any([word in message.content.casefold() for word in config['words']]):
        if (random.randint(1, 2) == 1):
            await channel.send('{} {}'.format(message.author.mention, config['response']))
            return

    if any([word in message.content.casefold() for word in config['words3']]):
        await channel.send('{} {}'.format(message.author.mention, config['response3']))
        return

    if any([word in message.content.casefold() for word in config['words4']]):
        await channel.send('{} {}'.format(message.author.mention, config['response4']))
        return

    if any([word in message.content.casefold() for word in config['words5']]):
        if (random.randint(1, 2) == 1):
            await channel.send('{} {}'.format(config['response5'], message.author.mention))
            return
        else:
            await channel.send('{} {}'.format(config['response5.5'], message.author.mention))
            return

    if any([word in message.content.casefold() for word in config['words6']]):
        await channel.send('{}'.format(config['response6']))
        return

    if any([word in message.content.casefold() for word in config['words7']]):
        wordList = config['words7']
        wordPosBool = ([word in message.content.casefold() for word in config['words7']])
        lengthOfList = len(wordList)
        for x in range(0, lengthOfList):
            if (wordPosBool[x] == True):
                Word = wordList[x]
                await channel.send('{} {}'.format(Word, config['response7']))
                return
                #elif (randNum == 2):
                    #await channel.send('{}'.format("https://tenor.com/view/touchdown-bruh-really-gif-12484222"))
                    #return
                #else:
                    #await channel.send('{}'.format("https://tenor.com/view/bruh-gif-5156041"))
                    #return

    if any([word in message.content.casefold() for word in config['words8']]):
        if (random.randint(1, 3) == 1):
            await channel.send('{}'.format(config['response8']))
            return
        else:
            await channel.send('{}'.format("wat"))
            return


    if any([word in message.content.casefold() for word in config['words9']]):
        wordList = config['words9']
        wordPosBool = ([word in message.content.casefold() for word in config['words9']])
        lengthOfList = len(wordList)
        for x in range(0, lengthOfList):
            if (wordPosBool[x] == True):
                Word = wordList[x]
                await channel.send('{} {} {} {}'.format(message.author.mention, config['response9'], Word, config['response9.5']))
                return

    if any([word in message.content.casefold() for word in config['words10']]):
        await channel.send('{}'.format("why are u gay"))
        return

    if any([word in message.content.casefold() for word in config['words12']]):
        wordList = config['words12']
        wordPosBool = ([word in message.content.casefold() for word in config['words12']])
        lengthOfList = len(wordList)
        for x in range(0, lengthOfList):
            if (wordPosBool[x] == False):
                Word = wordList[x]
                if (random.randint(1, 2) == 1):
                    await channel.send('{} {}{}'.format("On what,",Word,"?"))
                    return
    
    if any([word in message.content.casefold() for word in config['ok']]):
        await channel.send('{}'.format("ok"))
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
