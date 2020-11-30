from discord.ext import commands
import discord
import aiohttp
import io
import os


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
