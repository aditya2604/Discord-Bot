import json
import random
from datetime import datetime
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
client = discord.Client(description=desc)

@client.event
async def on_message(message: discord.Message):
    channel = message.channel
    username = message.author.name

    if (username == "Blueface"):
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
        else:
            await channel.send('{}'.format("https://tenor.com/view/watch-your-profanity-funny-gif-5600117"))
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
        elif (random.randint(1, 2) == 1):
            await channel.send('{}'.format("https://tenor.com/view/6ix9ine-big-mad-gooba-snitch-he-is-back-gif-17173480"))
            return
        else:
            await channel.send('{} {}'.format(config['response5.5'], message.author.mention))
            return

    if any([word in message.content.casefold() for word in config['words6']]):
        await channel.send('{}'.format(config['response6']))
        return

    if any([word in message.content.casefold() for word in config['words7']]):
        wordList = config['words7']
        wordPosBool = ([word in message.content.casefold()
                        for word in config['words7']])
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
        if (random.randint(1, 2) == 1):
            await channel.send('{}'.format(config['response8']))
            return
        else:
            if (random.randint(1, 2) == 1):
                await channel.send('{}'.format("https://tenor.com/view/blueface-fixing-eye-brow-preparing-gif-13523555"))
                return
            else:
                await channel.send('{}'.format("https://tenor.com/view/yeah-aight-blueface-nod-nodding-gif-13272333"))
                return

    if any([word in message.content.casefold() for word in config['words9']]):
        wordList = config['words9']
        wordPosBool = ([word in message.content.casefold()
                        for word in config['words9']])
        lengthOfList = len(wordList)
        for x in range(0, lengthOfList):
            if (wordPosBool[x] == True):
                Word = wordList[x]
                await channel.send('{} {} {} {}'.format(message.author.mention, config['response9'], Word, config['response9.5']))
                return

    if any([word in message.content.casefold() for word in config['words10']]):
        await channel.send('{}'.format("https://tenor.com/view/whyareyougay-uganda-gay-gif-14399349"))
        return

    if any([word in message.content.casefold() for word in config['words11']]):
        if (random.randint(1, 2) == 1):
            await channel.send('{}'.format("https://media.tenor.com/images/05de333b038141f6b8208c7ce8f8613c/tenor.gif"))
            return
        else: 
            return

    if any([word in message.content.casefold() for word in config['words12']]):
        wordList = config['words12']
        wordPosBool = ([word in message.content.casefold()
                        for word in config['words12']])
        lengthOfList = len(wordList)
        for x in range(0, lengthOfList):
            if (wordPosBool[x] == False):
                Word = wordList[x]
                if (random.randint(1, 2) == 1):
                    await channel.send('{}'.format("https://tenor.com/view/buss-down-blueface-rap-gif-14646202"))
                    return
                else:
                    await channel.send('{} {}{}'.format("On what,",Word,"?"))
                    return

@client.event
async def on_ready():
    app_info = await client.application_info()
    client.owner = app_info.owner
    print('Bot: {0.name}:{0.id}'.format(client.user))
    print('Owner: {0.name}:{0.id}'.format(client.owner))
    print('------------------')
    perms = discord.Permissions.none()
    perms.administrator = True
    url = discord.utils.oauth_url(app_info.id, perms)
    print('To invite me to a server, use this link\n{}'.format(url))

    #GAMEactivity
    game = discord.Game(name="with the homies", state="In Game")
    await client.change_presence(activity=game, status=discord.Status.dnd)

    #STREAMactivity
    #stream = discord.Streaming(platform="YouTube", name="Learn The Alphabet with Ugandan Pasta Senpai", url="https://www.youtube.com/watch?v=D6EmT8FwAgo", details="Learn The Alphabet with Ugandan Pasta Senpai") 
    #await client.change_presence(activity=stream)

    #WATCHactivity
    #watch = discord.Activity(type=discord.ActivityType.watching, name="video")
    #await client.change_presence(activity=watch, status=discord.Status.idle)

    #LISTENINGactivity
    #listen = discord.Activity(type=discord.ActivityType.listening, name="music")
    #await client.change_presence(activity=listen, status=discord.Status.idle)

if __name__ == '__main__':
    try:
        client.run(config['discord_token'])
    except KeyError:
        print("config not yet filled out.")
    except discord.errors.LoginFailure as e:
        print("Invalid discord token.")
