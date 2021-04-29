import discord
from discord import utils, File, Embed
from discord.ext import commands

from datetime import datetime, timedelta
import asyncio

import os
from dotenv import load_dotenv

load_dotenv()


awards_dict = {
    "meme": {
        "channel": 689401725005725709,
        # "emoji": 770733860308516924,
        "emoji": 818791635071795241,
    },
    "quote": {
        "channel": 689933365645803603,
        # "emoji": 782328811475173407,
        "emoji": 818791635529891870,
    }
}


class Awards(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="awards", aliases=["award"])
    @commands.check(commands.has_role(int(os.getenv("DISCORD_ROLE_VIKINGRALLY"))))
    async def awards(self, ctx, award: str, period: str = "current", top_x: int = 10):
        if award not in list(awards_dict.keys()):
            raise commands.BadArgument(f"{award} is not a valid argument")

        channel = utils.get(ctx.guild.channels, id=awards_dict[award]["channel"])
        emoji = utils.get(ctx.guild.emojis, id=awards_dict[award]["emoji"])

        now = datetime.utcnow()

        if period == "current":
            start = datetime(now.year, now.month, 1, 0, 0, 0)
            end = now

        elif period == "last":
            month = (now.month - 1 + 12) % 12
            year = now.year
            if month > now.month:
                year -= 1

            start = datetime(year, month, 1, 0, 0, 0)
            end = datetime(now.year, now.month, 1, 0, 0, 0)

        else:
            raise commands.errors.BadArgument(f"{period} is not a valid argument")

        if start.month == 3:  # BST starts
            end += timedelta(hours=1)
        elif start.month == 10:  # BST ends
            start += timedelta(hours=1)
        elif 3 < start.month < 10:  # BST happening
            start += timedelta(hours=1)
            end += timedelta(hours=1)

        print(start)
        print(end)
        print(emoji)

        messages = {}
        async for message in channel.history(after=start, before=end):
            for reaction in message.reactions:
                if reaction.emoji is emoji:
                    counter = 0
                    async for user in reaction.users():
                        if not user.bot:
                            counter += 1
                    messages[message.id] = counter
        sorted_messages = {k: v for k, v in sorted(messages.items(), key=lambda item: item[1], reverse=True)}

        print(len(messages))

        def check(reaction, user):
            print(user == ctx.author)
            print(str(reaction.emoji) == "👎")
            return user == ctx.author and str(reaction.emoji) == "👎"

        allowed_mentions = discord.AllowedMentions.none()

        total_count = len([(k, v) for k, v in sorted_messages.items()])
        nonzero_count = len([(k, v) for k, v in sorted_messages.items() if v > 0])

        embed = Embed(title=f"Top {top_x} {award.title()}s for {start.strftime('%B')}")

        i = 1
        for message_id in list(sorted_messages.keys()):
            if i > top_x:
                break
            message = await channel.fetch_message(message_id)
            points = sorted_messages[message_id]
            embed.add_field(name=f"#{i} - {points}", inline=False,
                            value=f"By {message.author.display_name} at {message.created_at.strftime('%D %X GMT')}"
                                  f"\n{message.clean_content}\n{message.jump_url}")
            i += 1
        embed.set_footer(text=f"Total {award}s = {total_count}. {award.title()}s with a reaction = {nonzero_count}")
        embed.set_thumbnail(url=emoji.url)
        await ctx.send(embed=embed)

        # c = 1
        # while True:
        #     try:
        #         print(c - 1)
        #         print(len(list(sorted_messages.keys())))
        #         print(sorted_messages)
        #         print(list(sorted_messages.keys())[c - 1])
        #
        #         message_id = list(sorted_messages.keys())[c - 1]
        #         print(message_id, type(message_id))
        #         message = await channel.fetch_message(message_id)
        #         msg = await ctx.send(f"{message.jump_url}\n{message.author.display_name}\n{message.clean_content}",
        #                              allowed_mentions=allowed_mentions)
        #         for attachment in message.attachments:
        #             await ctx.send(attachment.url)
        #         await msg.wait_for("reaction_add", timeout=600.0, check=check)
        #         ctx += 1
        #     except KeyError:
        #         await ctx.send("No more messages found")
        #     except asyncio.TimeoutError:
        #         break

    async def on_message(self, message):
        guild = self.bot.get_guild(os.getenv("DISCORD_GUILD_SSAGO"))
        if message.channel.id == awards_dict["meme"]["channel"] and len(message.attachements) != 0:
            emoji = utils.get(guild.emojis, id=awards_dict["meme"]["emoji"])
        elif message.channel.id == awards_dict["quote"]["channel"] and len(message.mentions) != 0:
            emoji = utils.get(guild.emojis, id=awards_dict["quote"]["emoji"])
        else:
            return
        await message.add_reaction(emoji)
