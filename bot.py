from discord.ext import commands
import discord

from cogs import basic_cog, catch_cog, famous_vikings_cog, meme_cog, translate_cog, birthday_cog
from discord import Color
from pretty_help import PrettyHelp

import os
from dotenv import load_dotenv
import logging

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
        self.add_cog(basic_cog.Basic())
        self.add_cog(translate_cog.Translate())
        self.add_cog(catch_cog.Catch())
        self.add_cog(famous_vikings_cog.FamousVikings())
        self.add_cog(meme_cog.Meme(self))
        # self.add_cog(birthday_cog.Birthday(database))  # Currently Disabled due to poor design

    # Error Handling (In the loosest sense of the word). Errors get sent to log
    async def on_command_error(self, ctx, exception):
        if isinstance(exception, commands.errors.MissingRequiredArgument):  # Capture for missing argument error
            await ctx.send('Å nei!, You\'ve missed a required argument for this command! This command will have its own'
                           ' help argument, so type it again with help before it!')
        else:
            await ctx.send('Å nei!, somethings gone wrong here. You\'ve either encountered a bug or the command you'
                           ' entered dosen\'t exist! I\'ve sent more info about what\'s gone wrong to my developers so'
                           ' they can work this out')
        await self.get_user(689579955012632586).send(f'%(asctime)s:%(levelname)s:%(name)s: %(message)s')

        logger.error(exception)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.get_user(689579955012632586).send(f"{os.path.abspath(os.curdir)}")


# Load discord token from .env file
TOKEN = os.getenv('DISCORD_TOKEN')

# Start Bjorn Running
bjorn = Bjorn()
bjorn.run(TOKEN)
