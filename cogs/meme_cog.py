from discord.ext import commands
import discord
import aiohttp
import io
import os
import praw
import random
from dotenv import load_dotenv


class Meme(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        ctx = await self.bot.get_context(message)

        if ctx.channel.type == discord.ChannelType.private:
            guild = self.bot.get_guild(689381329535762446)  # gets SSAGO server
            role = guild.get_role(699975448263786558)  # gets Viking Rally role
            if role in guild.get_member(ctx.author.id).roles:  # only allows Viking Rally committee past
                if message.author.bot:  # prevent a bot from triggering it, including self-triggering
                    return
                elif len(message.attachments) > 0 and message.content == "Meme":
                    for attachment in message.attachments:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(attachment.url) as resp:
                                if resp.status != 200:
                                    return await message.channel.send("Could not download file...")
                                data = io.BytesIO(await resp.read())
                                channel = self.bot.get_channel(689401725005725709)  # SSAGO meme channel
                                await channel.send(file=discord.File(data, os.path.basename(attachment.url)))

    @commands.command(name="meme")
    async def meme(self, ctx):
        await ctx.message.add_reaction("<viking:779801546002661447>")
        load_dotenv()
        reddit_id = os.getenv("REDDIT_ID")
        reddit_secret = os.getenv("REDDIT_SECRET")
        reddit_useragent = os.getenv("REDDIT_USERAGENT")
        reddit = praw.Reddit(client_id=reddit_id, client_secret=reddit_secret, user_agent=reddit_useragent)
        post_to_pick = random.randint(1, len(list(reddit.subreddit('vikingmemes').hot())))
        posts = reddit.subreddit('vikingmemes').hot()
        for i in range(0, post_to_pick):
            submission = next(post for post in posts if not post.stickied)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(submission.url) as resp:
                    if resp.status != 200:
                        return await ctx.send("Whoops, something's gone wrong...")
                    data = io.BytesIO(await resp.read())
                    await ctx.send(f"{submission.title}, courtesy of u/{submission.author}",
                                   file=discord.File(data, os.path.basename(submission.url)))
        except Exception as e:
            print(e)
