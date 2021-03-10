import asyncio

import discord
import youtube_dl

from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="joins a voice channel")
    async def join(self, ctx):
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            return await ctx.send('You need to be in a voice channel to use this command!')

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            vc = await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
            vc = ctx.voice_client
        self.queue = []
        await ctx.message.add_reaction('👍')

    @commands.command(description="streams music")
    async def play(self, ctx, *, url):
        self.voice_client = ctx.voice_client
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            if len(self.queue) == 0:
                await ctx.send("test")
                self.start_playing(voice_client, player)    
                embed = discord.Embed(title="Now playing", description=f"[{player.title}]({player.url}) [{ctx.author.mention}]")
            else:
                self.queue[len(self.queue)] = player
                embed = discord.Embed(title="", description=f"Queued [{player.title}]({player.url}) [{ctx.author.mention}]")
            await ctx.send(embed=embed)
        
    def start_playing(self, voice_client, player):
        self.queue[0] = player
        i = 0
        while i < len(self.queue):
            self.voice_client.play(self.queue[i], after=lambda e: print('Player error: %s' % e) if e else None)
            i+=1
    
    @commands.command(description="pauses music")
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("Paused ⏸️")
    
    @commands.command(description="resumes music")
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("Resuming ⏯️")

    @commands.command(description="stops and disconnects the bot from voice")
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.message.add_reaction('👋')

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

def setup(bot):
    bot.add_cog(Music(bot))