from discord.ext import commands

from cogs import basic_cog, translate_cog

import os
from dotenv import load_dotenv
import logging

# Set up error logger
logger = logging.getLogger('Discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class Bjorn(commands.Bot):

    def __init__(self):
        commands.Bot.__init__(self, command_prefix=commands.when_mentioned_or("Bjørn "), case_insensitive = True)

        # Add cogs here
        self.add_cog(basic_cog.Basic())
        self.add_cog(translate_cog.Translate())

    # Error Handling (In the loosest sense of the word). Errors get sent to log
    async def on_command_error(self, ctx, exception):
        await ctx.send('Å nei!, somethings gone wrong here. I\'ve sent more info about what\'s gone wrong to my developers so they can work this out')
        logger.error(exception)

# Load discord token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Start Bjorn Running
bjorn = Bjorn()
bjorn.run(TOKEN)