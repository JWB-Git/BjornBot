from discord.ext import commands
import discord

from cogs import basic_cog, catch_cog, famous_vikings_cog, meme_cog, translate_cog, birthday_cog, awards_cog
from discord import Color
from pretty_help import PrettyHelp

import os
from dotenv import load_dotenv
import logging
import traceback
import socket

import datetime
import random

# import pyrebase  # Currently disabled as not needed due to disabled birthday feature

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Set up error logger
logger = logging.getLogger('Discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename=os.path.join(os.curdir, 'discord.log'), encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()


class Bjorn(commands.Bot):

    def __init__(self):
        intents = discord.Intents.all()
        commands.Bot.__init__(self, command_prefix=commands.when_mentioned_or("Bjørn "), case_insensitive=True,
                              help_command=PrettyHelp(color=Color.purple(), show_index=False), intents=intents)

        # Set up Firebase Database
        # Currently disabled as not needed due to disabled birthday feature
        # config = {
        #     'apiKey': os.getenv('FIREBASE_API_KEY'),
        #     'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
        #     'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
        #     'databaseURL': os.getenv('FIREBASE_DATABASE_URL')
        # }
        # firebase = pyrebase.initialize_app(config)
        # database = firebase.database()

        # Add cogs here
        self.add_cog(basic_cog.Basic(self))
        self.add_cog(translate_cog.Translate())
        self.add_cog(catch_cog.Catch())
        self.add_cog(famous_vikings_cog.FamousVikings())
        self.add_cog(meme_cog.Meme(self))
        self.add_cog(awards_cog.Awards(self))
        # self.add_cog(birthday_cog.Birthday(database))  # Currently Disabled due to poor design
        
    async def pester(self):
        while True:
            dt = datetime.datetime.today().replace(hour=9, minute=0, second=0)
            random_time = random.random() * 21600  # 6 hour window so during opening hours
            now = datetime.datetime.now().timestamp() % 86400
            delay = dt + random_time - now
            if delay < 0:
                delay += 86400
            
            await bot.get_user(692814402960883775).send("This is your daily reminder to please sort out the Viking Rally "
                                                        "hoodies! 😊")
            guild = [guild for guild in bot.guilds if guild.id == 689381329535762446][0]
            channel = [channel for channel in guild.channels if channel.id == 699975897369018509][0]  # VR committee
            await channel.send("<@692814402960883775> this is your daily reminder to please sort out the Viking Rally "
                               "hoodies! 😊")

    # over-rides the default to allow commands to be triggered by other bots
    async def process_commands(self, message):
        ctx = await self.get_context(message)
        await self.invoke(ctx)

    # Error Handling (In the loosest sense of the word). Errors get sent to log
    async def on_command_error(self, ctx, exception):
        if isinstance(exception, commands.errors.MissingRequiredArgument):  # Capture for missing argument error
            await ctx.send('Å nei!, You\'ve missed a required argument for this command! This command will have its own'
                           ' help argument, so type it again with help before it!')
        elif isinstance(exception, (commands.errors.BadArgument, commands.errors.BadUnionArgument)):
            await ctx.send('Å nei!, You\'ve entered a bad argument for this command! This command will have its own'
                           ' help argument, so type it again with help before it!')
        elif isinstance(exception, commands.errors.MissingRole):  # Capture for the missing role error (e.g. for 'say')
            await ctx.send(f"Å nei!, You don't have the correct permissions to do that - naughty {ctx.author.mention}!")
        else:
            await ctx.send('Å nei!, somethings gone wrong here. You\'ve either encountered a bug or the command you'
                           ' entered dosen\'t exist! I\'ve sent more info about what\'s gone wrong to my developers so'
                           ' they can work this out')

            embed = discord.Embed(title="Error", description="Something's gone wrong...",
                                  colour=discord.Colour.from_rgb(113, 9, 170), url=ctx.message.jump_url)
            embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
            embed.add_field(name="Instance Hostname", value=socket.gethostname(), inline=False)
            embed.add_field(name="Author", value=f"{ctx.author.display_name}::{ctx.author.id}", inline=False)
            if ctx.guild:
                embed.add_field(name="Guild", value=f"{ctx.guild.name}::{ctx.guild.id}", inline=False)
                embed.add_field(name="Channel", value=f"{ctx.message.channel.name}::{ctx.message.channel.id}",
                                inline=False)
            else:
                embed.add_field(name="DM Channel", value=f"{ctx.channel.recipient}::{ctx.channel.id}", inline=False)
            embed.add_field(name="Message Content", value=ctx.message.content, inline=False)
            embed.add_field(name="Exception", value=exception, inline=False)
            embed.add_field(name="Traceback", value="To follow...", inline=False)
            embed.set_footer(text="Viking Rally - 19th to 21st November 2021 @ Moor House Adventure Centre, Durham",
                             icon_url="https://viking-rally.ssago.org/img/events/236/media/Viking%20Rally%20Logo.png")
            tb = "".join(traceback.format_exception(etype=type(exception), value=exception, tb=exception.__traceback__))

            await self.dev_send(embed=embed)
            await self.dev_send(f"```Python\n{tb}```")

        logger.error(exception)

    # Sends to appropriate developer or general channel, depending on which instance is running
    async def dev_send(self, content=None, *, tts=False, embed=None, file=None, files=None, delete_after=None,
                       nonce=None, allowed_mentions=None):
        if socket.gethostname() == os.getenv("HOSTNAME_TIM"):
            channel = self.get_user(int(os.getenv("DISCORD_ID_TIM")))
        elif socket.gethostname() == os.getenv("HOSTNAME_JACK"):
            channel = self.get_user(int(os.getenv("DISCORD_ID_JACK")))
        else:
            channel = self.get_channel(int(os.getenv("DISCORD_BJORN_CHANNEL")))
        await channel.send(content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after,
                           nonce=nonce, allowed_mentions=allowed_mentions)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.dev_send("[INFO] Hello, I'm back! :wave:")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print(payload)

        # checks if :x: emoji
        if payload.emoji.name != "❌":
            return

        # check if adding reaction, opposed to removing
        if payload.event_type != "REACTION_ADD":
            return

        channel = self.get_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)

        # checks if original message was sent by Bjørn
        if msg.author.id != int(os.getenv("DISCORD_ID_BJORN")):
            return

        guild = self.get_guild(int(os.getenv("DISCORD_GUILD_SSAGO")))
        bot_trainer = guild.get_role(int(os.getenv("DISCORD_ROLE_BOTTRAINER")))

        # checks if permission to remove message
        if payload.user_id not in [int(os.getenv("DISCORD_ID_TIM")), int(os.getenv("DISCORD_ID_JACK"))]:
            if payload.member:
                if bot_trainer in payload.member.roles:
                    pass
                else:
                    return
            else:
                return

        # prevent deletion in logging channel
        if payload.channel_id == int(os.getenv("DISCORD_BJORN_CHANNEL")):
            return

        user = self.get_user(payload.user_id)

        embed = discord.Embed(title="Info", description="Someone's deleted something I said...",
                              colour=discord.Colour.from_rgb(113, 9, 170), url=msg.jump_url)
        embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/2796/PNG/512/info_information_icon_178159.png")
        embed.add_field(name="Deleter", value=f"{user.display_name}::{user.id}", inline=False)
        if msg.guild:
            embed.add_field(name="Guild", value=f"{msg.guild.name}::{msg.guild.id}", inline=False)
            embed.add_field(name="Channel", value=f"{msg.channel.name}::{msg.channel.id}", inline=False)
        else:
            embed.add_field(name="DM Channel", value=f"{msg.channel.recipient}::{msg.channel.id}",
                            inline=False)
        embed.add_field(name="Message Content", value=msg.content, inline=False)
        embed.set_footer(
            text="Viking Rally - 19th to 21st November 2021 @ Moor House Adventure Centre, Durham",
            icon_url="https://viking-rally.ssago.org/img/events/236/media/Viking%20Rally%20Logo.png")

        channel = self.get_channel(int(os.getenv("DISCORD_BJORN_CHANNEL")))
        await channel.send(embed=embed)

        await msg.delete()


# Load discord token from .env file
TOKEN = os.getenv('DISCORD_TOKEN')

# Start Bjorn Running
bjorn = Bjorn()
bjorn.run(TOKEN)
