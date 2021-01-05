from discord.ext import commands
import discord
import datetime
import os
import dotenv
import asyncio

dotenv.load_dotenv()


class Leaderboards(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="leaderboard", brief="Get the latest leaderboards", help="Find out who's in the lead")
    async def leaderboard(self, ctx):
        embed = discord.Embed(title="Let's get this leaderboard made...")
        embed.set_footer(text="Viking Rally - 19th to 21st November 2021 @ Moor House Adventure Centre, Durham",
                         icon_url="https://viking-rally.ssago.org/img/events/236/media/Viking%20Rally%20Logo.png")
        msg = await ctx.send(embed=embed)
        if not ctx.invoked_subcommand:
            channels = [self.bot.get_channel(os.getenv(f"DISCORD_CHANNEL_{x}")) for x in ["MEMES", "QUOTES"]]
            if ctx.channel in channels:
                channel = ctx.channel
            else:
                raise commands.MissingRequiredArgument(f"My simple leaderboard only works in {channels[0].mention} and "
                                                       f"{channels[1].mention}")

            timeframe = "month"
            board_type = "individual"
            top = 5
            bot = "neither"

    @leaderboard.command(name="advanced", brief="Advanced version of the leaderboard",
                         help="Use various options to customise the leaderboard to your liking")
    async def advanced(self, ctx):
        embed = discord.Embed(title="Let's get this leaderboard made...")
        embed.set_footer(text="Viking Rally - 19th to 21st November 2021 @ Moor House Adventure Centre, Durham",
                         icon_url="https://viking-rally.ssago.org/img/events/236/media/Viking%20Rally%20Logo.png")
        message = await ctx.send(embed=embed)
        channel = await self.get_leaderboard_channel(message)
        if channel is not None:
            timeframe = await self.get_leaderboard_timeframe(message)
            if timeframe is not None:
                board_type = await self.get_leaderboard_type(message)
                if board_type is not None:
                    top = await self.get_leaderboard_top(message)
                    if top is not None:
                        bot = self.get_leaderboard_bot(message)
        # return

        async def get_leaderboard_channel(msg):
            embed.add_field(name="Please choose what you'd like a leaderboard for",
                            value=":one: Memes\n:two: Quotes")
            field_index = len(embed.fields) - 1
            msg.edit(embed=embed)
            # msg.edit(content="Please choose if you'd like a leaderboard for:\n:one: Memes\n:two: Quotes")
            await msg.add_reaction(":one:")
            await msg.add_reaction(":two:")

            def check(reaction_to_check, user_to_check):
                return user_to_check == ctx.author and str(reaction_to_check.emoji) in [":one:", ":two:"]

            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
            except asyncio.TimeoutError:
                embed.set_field_at(field_index, name=embed.fields[field_index],
                                   value="Sorry, you've taken too long to tell me what to do :cry:")
                msg.edit(embed=embed)
                # await msg.edit(content="Sorry, you've taken too long to tell me what to do :cry:")
            else:
                await msg.clear_reactions()
                if str(reaction) == ":one:":
                    embed.set_field_at(field_index, name=embed.fields[field_index],
                                       value="You've chosen the Meme leaderboard")
                    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/770733860308516924.png")
                    msg.edit(embed=embed)
                    return self.bot.get_channel(os.getenv("DISCORD_CHANNEL_MEMES"))
                elif str(reaction) == ":two:":
                    embed.set_field_at(field_index, name=embed.fields[field_index],
                                       value="You've chosen the Quote leaderboard")
                    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/782328811475173407.png")
                    msg.edit(embed=embed)
                    return self.bot.get_channel(os.getenv("DISCORD_CHANNEL_QUOTES"))

        async def get_leaderboard_timeframe(msg):
            embed.add_field(name="Please choose the timeframe for your leaderboard",
                            value=":one: Current month\n:two: All time")
            field_index = len(embed.fields) - 1
            msg.edit(embed=embed)
            # msg.edit(content="Please choose the timeframe for your leaderboard:\n:one: Current month\n:two: All time")
            await msg.add_reaction(":one:")
            await msg.add_reaction(":two:")

            def check(reaction_to_check, user_to_check):
                return user_to_check == ctx.author and str(reaction_to_check.emoji) in [":one:", ":two:"]

            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
            except asyncio.TimeoutError:
                # await msg.edit(content="Sorry, you've taken too long to tell me what to do :cry:")
                embed.set_field_at(field_index, name=embed.fields[field_index],
                                   value="Sorry, you've taken too long to tell me what to do :cry:")
                msg.edit(embed=embed)
            else:
                await msg.clear_reaction()
                if str(reaction) == ":one:":
                    embed.set_field_at(field_index, name=embed.fields[field_index],
                                       value="You've chosen the current month")
                    msg.edit(embed=embed)
                    return "month"
                elif str(reaction) == ":two:":
                    embed.set_field_at(field_index, name=embed.fields[field_index],
                                       value="You've chosen all time")
                    msg.edit(embed=embed)
                    return "all"

        async def get_leaderboard_type(msg):
            embed.add_field(name="Please choose the couting method for your leaderboard",
                            value=":one: Individual\n:two: Cumulative")
            field_index = len(embed.fields) - 1
            msg.edit(embed=embed)
            # msg.edit(content="Please choose the counting method for your leaderboard:\n:one: Individual\n:two: Cumulative")
            await msg.add_reaction(":one:")
            await msg.add_reaction(":two:")

            def check(reaction_to_check, user_to_check):
                return user_to_check == ctx.author and str(reaction_to_check.emoji) in [":one:", ":two:"]

            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
            except asyncio.TimeoutError:
                embed.set_field_at(field_index, name=embed.fields[field_index],
                                   value="Sorry, you've taken too long to tell me what to do :cry:")
                msg.edit(embed=embed)
                # await msg.edit(content="Sorry, you've taken too long to tell me what to do :cry:")
            else:
                await msg.clear_reaction()
                if str(reaction) == ":one:":
                    return "individual"
                elif str(reaction) == ":two:":
                    return "cumulative"

        async def get_leaderboard_top(msg):
            msg.edit(content="Please choose the top X submissions you'd like to have displayed:\n:one:-:keycap_ten: are simply their numerical values\n:infinity: shows all that have a least one vote")
            options = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "keycap_ten": 10, "infinity": 0}
            for i in options.keys():
                await msg.add_reaction(f":{i}:")

            def check(reaction_to_check, user_to_check):
                return user_to_check == ctx.author and str(reaction_to_check.emoji) in [f":{option}:" for option in options.keys()]

            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await msg.edit(content="Sorry, you've taken too long to tell me what to do :cry:")
            else:
                await msg.clear_reaction()
                return options[str(reaction)]


        async def get_leaderboard_bot(msg):
            msg.edit(content="Please choose if you would like submissions from bots and/or Tom Webster included:\n:one: No to both\n:two: Yes to bots, no to Tom\n:three: No to bots, yes to Tom\n:four: Yes to both")
            await msg.add_reaction(":one:")
            await msg.add_reaction(":two:")
            await msg.add_reaction(":three")
            await msg.add_reaction("four")

            def check(reaction_to_check, user_to_check):
                return user_to_check == ctx.author and str(reaction_to_check.emoji) in [":one:", ":two:", "three", "four"]

            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await msg.edit(content="Sorry, you've taken too long to tell me what to do :cry:")
            else:
                await msg.clear_reaction()
                if str(reaction) == ":one:":
                    return "neither"
                elif str(reaction) == ":two:":
                    return "bots"
                elif str(reaction) == ":three:":
                    return "tom"
                elif str(reaction) == ":four:":
                    return "both"

    channel = await self.get_leaderboard_channel(message)
    if channel is not None and advanced:
        timeframe = await get_leaderboard_timeframe(message)
        if timeframe is not None:
            board_type = await get_leaderboard_type(message)
            if board_type is not None:
                top = await get_leaderboard_top(message)
                if top is not None:
                    bot = get_leaderboard_bot(message)
    elif not advanced:
        timeframe = "month"
        board_type = "individual"
        top = 5
        bot = "neither"

    now = datetime.datetime.now()

    if timeframe == "month":
        start = datetime.datetime(now.year, now.month, 1)
        end = start.replace(month=((start.month + 1) % 12))
        if end.month == 1:
            end = end.replace(year=start.year + 1)
    elif timeframe == "all":
        start = datetime.datetime
        end = now

    leaderboard_emoji = {689401725005725709: 783289832876802049,  # memes
                         689933365645803603: 783126117502550027}  # quotes
    r = await channel.fetch_message(leaderboard_emoji[channel.id]).reactions[0]


    entries = {}
    async for message in channel.history(limit=None, after=start, before=end):
        if (channel.id == os.getenv("DISCORD_CHANNEL_QUOTES") and len(message.mentions) > 0) or (channel.id == os.getenv("DISCORD_CHANNEL_MEMES") and len(message.attachments) > 0):
            for reaction in message.reactions:
                if reaction == r:
                    users = await reaction.users().flatten()
                    votes = len([user for user in users if not user.bot])

                    if board_type == "individual":
                        entries[message] = votes
                    elif board_type == "cumulative":
                        if message.author in entries.keys():
                            entries[message.author] += votes
                        else:
                            entries[message.author] = votes
    counter = 0
    last_value = 0
    rank = 1
    next_rank = 1
    top_x = 5
    embed = discord.Embed(title="Meme Spork Leadboard", description="Let's take a look at who's in the lead!",
                          colour=discord.Colour.from_rgb(113, 9, 170))
    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/770733860308516924.png")
    embed.set_footer(text="Viking Rally - 19th to 21st November 2021 @ Moor House Adventure Centre, Durham",
                     icon_url="https://viking-rally.ssago.org/img/events/236/media/Viking%20Rally%20Logo.png")
    await self.dev_send(embed=embed)
    for k, v in sorted(monthly_entries.items(), key=lambda item: item[1], reverse=True):
        # print(counter, last_value, rank, next_rank)
        if k.author.nick:
            name = k.author.nick
        else:
            name = k.author.name
        counter += 1
        if counter <= top_x and v >= last_value:
            print(rank, v, name, k.created_at, k.jump_url)
        elif counter <= top_x and v < last_value:
            rank = next_rank
            print(rank, v, name, k.created_at, k.jump_url)
        elif counter > top_x and v == last_value:
            print(rank, v, name, k.created_at, k.jump_url)
        elif counter > top_x and v < last_value:
            break
        last_value = v
        next_rank += 1
        embed = discord.Embed(title=f"#{rank}, with {v} vote(s)", description=name,
                              colour=discord.Colour.from_rgb(113, 9, 170), url=k.jump_url)
        embed.set_author(name="Meme Spork Leaderboard",
                         icon_url="https://cdn.discordapp.com/emojis/770733860308516924.png")
        embed.set_image(url=k.attachments[0].url)
        embed.set_footer(text="Viking Rally - 19th to 21st November 2021 @ Moor House Adventure Centre, Durham",
                         icon_url="https://viking-rally.ssago.org/img/events/236/media/Viking%20Rally%20Logo.png")
        await self.dev_send(embed=embed)
