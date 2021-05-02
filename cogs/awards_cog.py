from discord import utils, Embed
from discord.ext import commands

from datetime import datetime, timedelta

import os
from dotenv import load_dotenv

load_dotenv()


awards_dict = {
    "meme": {
        "channel": 689401725005725709,
        "emoji": 818791635071795241,
    },
    "quote": {
        "channel": 689933365645803603,
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

    @commands.Cog.listener()
    async def on_message(self, message):
        guild = self.bot.get_guild(int(os.getenv("DISCORD_GUILD_SSAGO")))
        if message.channel.id == awards_dict["meme"]["channel"] and len(message.attachments) != 0:
            emoji = utils.get(guild.emojis, id=awards_dict["meme"]["emoji"])
        elif message.channel.id == awards_dict["quote"]["channel"] and len(message.mentions) != 0:
            emoji = utils.get(guild.emojis, id=awards_dict["quote"]["emoji"])
        else:
            return
        await message.add_reaction(emoji)
