import discord
from discord.ext import commands 
import praw
import random

reddit = praw.Reddit(client_id = '3tNfOi1IwsvXqw',
                     client_secret = 'DfUdiixMoyFt0b5v_XkiBqzq6f9sCQ',
                     user_agent = 'Kermit discord bot (u/RoastSea8)', check_for_async=False)


class Meme(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(description="sends meme from r/memes")
    async def meme(self, ctx):
        subreddit = reddit.subreddit('memes')
        posts = subreddit.hot(limit=50)
        posts = list(posts)
        post = random.choice(posts)
        embed = discord.Embed(title=f"{post.title}", url=f"https://www.reddit.com{post.permalink})", description="", color=discord.Color.green())
        embed.set_image(url=post.url)
        embed.set_footer(text=f"👍 {post.score} | 💬 {post.num_comments}")
        await ctx.send(embed=embed)
    
    @commands.command(description="sends meme from r/facepalm")
    async def smh(self, ctx):
        subreddit = reddit.subreddit('facepalm')
        posts = subreddit.hot(limit=50)
        posts = list(posts)
        post = random.choice(posts)
        embed = discord.Embed(title=f"{post.title}", url=f"https://www.reddit.com{post.permalink})", description="", color=discord.Color.green())
        embed.set_image(url=post.url)
        embed.set_footer(text=f"👍 {post.score} | 💬 {post.num_comments}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Meme(bot))
