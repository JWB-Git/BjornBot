from discord.ext import commands
from discord import Embed, Colour, ChannelType, File, Status, utils, TextChannel, errors, Guild, CategoryChannel, VoiceChannel, Role, Member

from datetime import datetime, date

from math import floor

from random import randint

import json5
import json
import os
from dotenv import load_dotenv

import random
import giphy_client
from giphy_client.rest import ApiException

import re

from typing import Union

load_dotenv()


class Basic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello', aliases=['hi', 'hej', 'hei', 'halla' 'hallo', 'whyaye', 'why'],
                      brief="Say Hello to Bjorn", help="Say Hello to Bjorn")
    async def hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.mention}")

    @commands.command(name='countdown', brief="See how long until Viking Rally",
                      help="See how long until Viking Rally. If you put weeks, hours, minutes or seconds as a parameter"
                           " for the command, you can see how long it is in that time format!")
    async def countdown(self, ctx, unit='days'):
        viking_date = datetime(2021, 11, 19, 18, 00, 00)
        current_date = datetime.now()

        countdown = viking_date - current_date

        if unit == "days":
            await ctx.send(f"There are {countdown.days} more day(s) until Viking Rally 2021")
        elif unit == "weeks":
            await ctx.send(f"There are {countdown.days / 7} more week(s) until Viking Rally 2021")
        elif unit == "hours":
            await ctx.send(f"There are {floor(countdown.total_seconds() / 3600)} more hour(s) until Viking Rally 2021")
        elif unit == "minutes":
            await ctx.send(f"There are {floor(countdown.total_seconds() / 60)} more minutes(s) until Viking Rally 2021")
        elif unit == "seconds":
            await ctx.send(f"There are {floor(countdown.total_seconds())} more seconds(s) until Viking Rally 2021")

    @commands.command(name='info', aliases=['information', 'rally'], brief="Learn more about Viking Rally 2021",
                      help="Learn more about Viking Rally 2021")
    async def info(self, ctx, delete_after: int = None):
        embed = Embed(title="Viking Rally 2021", colour=Colour.from_rgb(113, 9, 170),
                      url="https://viking-rally.ssago.org")
        embed.set_image(url="https://viking-rally.ssago.org/img/events/236/media/Facebook%20Cover.png")
        embed.add_field(name="When is it?", value="19th - 21st November 2021", inline=False)
        embed.add_field(name="Where is it?", value="Moor House Adventure Centre, Durham", inline=False)
        embed.add_field(name="Who's running it?", value="NUSSAGG and DUSAGG", inline=False)
        embed.add_field(name="What makes it so special?",
                        value="It's the first SSAGO Rally in the North East for 21 Years!", inline=False)
        embed.set_footer(text="For more information about the Rally, click on 'Viking Rally 2021'",
                         icon_url="https://viking-rally.ssago.org/img/events/236/media/Viking%20Rally%20Logo.png")

        await ctx.send(embed=embed, delete_after=delete_after)

    @commands.command(name='egm', brief="Learn about the EGM",
                      help="Learn more about the Extrodenary General Meeting")
    async def egm(self, ctx, delete_after: int = None):
        embed = Embed(title="Extrodenary General Meeting", colour=Colour.from_rgb(0, 154, 68),
                      url="https://vote.ssago.org/")
        embed.set_thumbnail(url="https://www.ssago.org/img/ssago.png")
        embed.add_field(name="When is it?", value="Sunday 18th of July 2021", inline=False)
        embed.add_field(name="What's it for?", value="To elect a SSAGO Ball for Spring 2022, and maybe more (tbc)",
                        inline=False)
        embed.add_field(name="Why?", inline=False,
                        value="The Exec have decided to hold the EGM at this time to allow sufficient time for the "
                              "SSAGO Ball 2022 to be elected and organised. It's appreciated this is still a short "
                              "turnaround compared to historical SSAGO Balls so it's encouraged those who may want to "
                              "bid for a ball to think outside the box.")
        # embed.set_footer(text="For more information about the Rally, click on 'Viking Rally 2021'",
        #                  icon_url="https://viking-rally.ssago.org/img/events/236/media/Viking%20Rally%20Logo.png")

        await ctx.send(embed=embed, delete_after=delete_after)

    @commands.command(name='dev', aliases=['devs', 'development', 'git', 'github', 'code'],
                      brief="See my developers and code!", help="See my developers and code!")
    async def dev(self, ctx):
        embed = Embed(title="BjornBot", colour=Colour.from_rgb(113, 9, 170),
                      url="https://github.com/JWB-Git/BjornBot")

        embed.add_field(name="Developed by", value="Jack Burgess and Tim Rodaway", inline=False)
        embed.add_field(name="Repo", value="Click on link in the title!", inline=False)
        embed.set_footer(text="Viking Rally - 19th to 21st November 2021 @ Moor House Adventure Centre, Durham",
                         icon_url="https://viking-rally.ssago.org/img/events/236/media/Viking%20Rally%20Logo.png")
        await ctx.send(embed=embed)

    @commands.command(name='steal', brief="Try to steal me!", help="Try to steal me!")
    async def steal(self, ctx):
        with open("data/steal_statements.json", "r") as jsonFile:
            data = json.load(jsonFile)

        if not os.path.exists("data/counters.json"):
            counters = {"steal": 0}
        else:
            with open("data/counters.json", "r") as jsonFile:
                counters = json.load(jsonFile)

        steal_counter = counters['steal']

        index = randint(0, len(data['statements']) - 1)

        if index == 0:
            steal_counter = steal_counter + 1
            counters['steal'] = steal_counter

            with open("data/counters.json", "w") as jsonFile:
                json.dump(counters, jsonFile)

        await ctx.send(data['statements'][index])
        await ctx.send(f'I have been stolen {steal_counter} times')

    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send("pong")

    # adds new check for devs, useful if not on SSAGO server
    def is_dev():
        def predicate(ctx):
            if ctx.author.id not in [int(os.getenv("DISCORD_ID_TIM")), int(os.getenv("DISCORD_ID_JACK"))]:
                raise commands.errors.MissingRole()
            return True

        return commands.check(predicate)

    @commands.command(name="say")
    # @commands.has_role(int(os.getenv("DISCORD_ROLE_VIKINGRALLY")))
    @commands.check_any(commands.has_role(int(os.getenv("DISCORD_ROLE_VIKINGRALLY"))), is_dev())
    async def say(self, ctx, *, arg: str):
        await ctx.send(arg)

    @commands.command(name="sayto")
    @commands.check_any(commands.has_role(int(os.getenv("DISCORD_ROLE_VIKINGRALLY"))), is_dev())
    async def sayto(self, ctx, channel_id: int, *, arg: str):
        channel = self.bot.get_channel(channel_id)
        if channel is not None:
            try:
                await channel.send(arg)
            except errors.Forbidden:
                await ctx.send(f"Unfortunately I can't send stuff to {channel.name} :cry:")
        else:
            ctx.send(f"Unable to find channel with ID {channel_id}.")

    @commands.command(name="im")
    @commands.check_any(commands.has_role(int(os.getenv("DISCORD_ROLE_VIKINGRALLY"))), is_dev())
    async def im(self, ctx, channel_id: int, message_id: int):
        channel = self.bot.get_channel(channel_id)
        if channel is not None:
            try:
                message = await channel.fetch_message(message_id)
                for i in range(len(message.content[message.content.lower().index("i'm") + 3:].split("."))):
                    im = message.content[message.content.lower().index("i'm") + 3:].split(".")[i]
                    print("*" + im + "*")
                    if not re.compile("^\s*$").match(im):
                        print("breaking")
                        break

                delete_after = 60

                # await message.reply(f"Hi{im}, I'm Bjørn! Have you heard about Viking Rally?")
                await message.reply(f"Hi{im}, I'm Bjørn! Have you heard about the SSAGO EGM?")

                if message.guild.id == 689381329535762446 and \
                        message.guild.get_role(689383534208614409) in message.author.roles:  # Exec role
                        # message.guild.get_role(699975448263786558) in message.author.roles:  # Viking Rally role
                    await message.channel.send("Oh yeah, of course you do, you're helping organise it! Anyhow, no time "
                                               "like the present for some promotion.", delete_after=delete_after)

                if not (datetime.now().month == 2 and datetime.now().year == 2021):
                    await self.egm(message.channel, delete_after=delete_after)

                # torments Nathan
                if message.author.id == int(os.getenv("DISCORD_ID_NATHAN")):
                    nathan = self.bot.get_user(int(os.getenv("DISCORD_ID_NATHAN")))
                    try:
                        query = "mwahahaha"
                        gifs = giphy_client.DefaultApi().gifs_search_get(os.getenv("GIPHY_TOKEN"), query, limit=10,
                                                                         rating='g')
                        lst = list(gifs.data)
                        gif = random.choices(lst)[0].url
                        await nathan.send(gif)
                        await nathan.send(file=File("GIPHY.gif"))
                    except ApiException as e:
                        return f"Exception when calling DefaultApi->gifs_search_get: {e}\n"
            except errors.NotFound:
                ctx.send(f"Unable to find message with ID {message_id}.")
            except errors.Forbidden:
                await ctx.send(f"Unfortunately I can't send stuff to {channel.name} :cry:")
        else:
            ctx.send(f"Unable to find channel with ID {channel_id}.")

    @commands.command(name="survey", brief="Pre-Raid Survey", help="Get a link to Viking Rally's Pre-Raid Survey")
    async def survey(self, ctx):
        if datetime.now().month == 2 and datetime.now().year == 2021:
            await ctx.send("You can find our pre-raid survey on the Viking Rally event site, over at "
                           "https://viking-rally.ssago.org/pages/survey. It's open til the end of the month, so please "
                           "do fill it out! :grin:")
        else:
            await ctx.send("Sadly you've missed our survey, as it was only open until the end of February :cry:")

    @commands.command(name="permissions", brief="Get permissions of a channel",
                      help="Get the permissions of a specific channel")
    async def permissions(self, ctx: commands.Context, channel: Union[TextChannel, CategoryChannel]):
        embed = Embed(title=f"Permission Overwrites for {channel.type} channel '{channel.name}' in '{channel.guild}'")
        for k, v in channel.overwrites.items():
            if isinstance(k, Role):
                display = f"Role: {k.name}"
            else:
                display = f"Member: {k.display_name}"
            embed.add_field(name=display, inline=False,
                            value="\n".join([f"{perm}: {value}" for perm, value in iter(v) if value is not None]))
        await ctx.send(embed=embed)

    @commands.command(name="rolees", brief="All members in a role", help="Get a list of all members within a role")
    async def rolees(self, ctx: commands.Context, role_argument: str, guild_argument=None):
        print(role_argument)
        print(guild_argument)
        if guild_argument is None:
            role = await commands.RoleConverter().convert(ctx, role_argument)
            guild: Guild = ctx.guild
        else:
            guild = await commands.GuildConverter().convert(ctx, guild_argument)
            print(type(guild))
            match = re.match(r'([0-9]{15,21})$', role_argument) or re.match(r'<@&([0-9]+)>$', role_argument)
            if match:
                role = guild.get_role(int(match.group(1)))
            else:
                role = utils.get(guild.roles, name=role_argument)
            if role is None:
                raise commands.errors.RoleNotFound(role_argument)
        embed = Embed(title=f"Holders of the role '{role}' in '{role.guild}'", colour=role.colour)
        d = {}
        for member in role.members:
            top_hoist_role = guild.default_role
            for role in member.roles[::-1]:
                if role.hoist:
                    top_hoist_role = role
                    break
            d[top_hoist_role] = list(d.get(top_hoist_role, "")) + [member]
        sorted_d = {k: v for k, v in sorted(d.items(), key=lambda items: items[0].position, reverse=True)}
        for k, v in sorted_d.items():
            embed.add_field(name=k, inline=False, value="\n".join([member.display_name for member in v]))
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text=f"{len(role.members)} members have this role\n{role.name}:{role.id}")
        await ctx.send(embed=embed)

    @commands.command(name="structure", brief="Show server structure",
                      help="Shows you a list of all the channels in the server, arranged by category")
    async def structure(self, ctx: commands.Context, *, guild: Guild):
        if not guild:
            guild = ctx.guild
        d = {}
        for category in guild.categories:
            d[category] = []
        for channel in guild.text_channels + guild.voice_channels:
            d[channel.category] = list(d.get(channel.category, "")) + [channel]
        sorted_d = {k: v for k, v in sorted(d.items(), key=lambda items: items[0].position, reverse=False)}
        await ctx.send(f"**Structure of channels in '{guild}'**")
        for category, channels in sorted_d.items():
            list_of_channels = []
            for channel in channels:
                channel_string = ""
                if isinstance(channel, TextChannel):
                    channel_string += "📝"
                    if channel.is_nsfw():
                        channel_string += "🔞"
                elif isinstance(channel, VoiceChannel):
                    channel_string += "🎤"
                else:
                    channel_string += "❓"
                channel_string += f": {channel.name}"
                list_of_channels.append(channel_string)
            channels_string = "\n".join(list_of_channels)
            await ctx.send(f"\n\n***{category.name}***\n{channels_string}")
        await ctx.send("*** Done ***")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Viking Rally Emoji React
        if re.compile(r"(^(rally|viking|rallies)\W|\W(rally|viking|rallies)$|^(rally|viking|rallies)$|\W(rally|viking|"
                      r"rallies)\W)").match(message.content.lower()):
            await message.add_reaction('<:viking:779801546002661447>')

        # Added a Viking Rally react and Meme Spork react to any memes the Viking Rally committee post
        if (message.channel.id == 689401725005725709) and \
                (message.guild.get_role(699975448263786558) in message.author.roles) and (len(message.attachments) > 0):
            await message.add_reaction('<:viking:779801546002661447>')
            await message.add_reaction('<memespork:770733860308516924>')

        # Axe react southampton members, we will not forget the shrimping, exempting Oli
        if (message.guild and not message.author.id == 678903558828982274 and message.guild.get_role(692795753168634006)
            in message.author.roles and randint(0, (date.today() - date(2021, 2, 22)).days) == 0) \
                or message.author.id == 150339580359475200:
            await message.add_reaction("🐬")
            await message.add_reaction("🪓")

        # Hi <Name>, I'm Bjørn
        # Inspired by Nathan Flaherty of BUSAG, who uses this dad joke at literally every opportunity!
        if "i'm" in message.content.lower() and not message.author.bot:

            # prevents dad jokes in DMs or error logging channel to keep it neat
            if (message.channel.type is ChannelType.private) or \
                    (message.channel.id == int(os.getenv("DISCORD_BJORN_CHANNEL"))):
                return

            spam_role = utils.get(message.guild.roles, name="botspam")
            spam_allowed = True
            if spam_role:
                permissions = {perm: value for (perm, value) in iter(message.channel.overwrites_for(spam_role))}
                permission = permissions["send_messages"]
                if permission is False:
                    spam_allowed = False
            print(spam_allowed)

            # Will randomly reply to 1 in 20 I'm messages
            if ((randint(0, 19) == 0) or (message.author.id == int(os.getenv("DISCORD_ID_NATHAN")))) and spam_allowed:
                for i in range(len(message.content[message.content.lower().index("i'm") + 3:].split("."))):
                    im = message.content[message.content.lower().index("i'm") + 3:].split(".")[i]
                    print("*" + im + "*")
                    if not re.compile("^\s*$").match(im):
                        print("breaking")
                        break

                delete_after = 60

                if message.guild.id == 800488874803331123:
                    await message.channel.send(f"Hi{im}, I'm Bjørn!")

                else:
                    # await message.channel.send(f"Hi{im}, I'm Bjørn! Have you heard about Viking Rally?")
                    await message.channel.send(f"Hi{im}, I'm Bjørn! Have you heard about the SSAGO EGM?")

                # if message.guild.get_role(699975448263786558) in message.author.roles:  # Viking Rally role
                if message.guild.get_role(689383534208614409) in message.author.roles:  # Exec role
                    await message.channel.send("Oh yeah, of course you do, you're helping organise it! Anyhow, no time "
                                               "like the present for some promotion.", delete_after=delete_after)

                if not (datetime.now().month == 2 and datetime.now().year == 2021):
                    await self.egm(message.channel, delete_after=delete_after)

                # torments Nathan
                if message.author.id == int(os.getenv("DISCORD_ID_NATHAN")):
                    nathan = self.bot.get_user(int(os.getenv("DISCORD_ID_NATHAN")))
                    try:
                        query = "mwahahaha"
                        gifs = giphy_client.DefaultApi().gifs_search_get(os.getenv("GIPHY_TOKEN"), query, limit=10,
                                                                         rating='g')
                        lst = list(gifs.data)
                        gif = random.choices(lst)[0].url
                        await nathan.send(gif)
                        await nathan.send(file=File("GIPHY.gif"))
                    except ApiException as e:
                        return f"Exception when calling DefaultApi->gifs_search_get: {e}\n"

        # For the lols
        if message.author.id == 433626538316136448:  # Jess
            await message.add_reaction("🦀")
            await message.add_reaction("<a:animated_crab:811393820322955284>")
            if randint(1, 20) == 1:  # 1 in 20 times
                await message.author.send("https://music.youtube.com/watch?v=jhExvE5fvJw")  # Crab God video

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # Detects if Liam from Southampton comes online
        if before.id == 150339580359475200 and before.status == Status.offline and before.status != after.status:
            await after.send("This is what you get for messing with the Vikings...")
            await after.send("<:Decapitated_Phillipa:813406341749145691>")
