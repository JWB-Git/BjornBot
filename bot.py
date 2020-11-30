from discord.ext import commands
import discord

from cogs import basic_cog, catch_cog, famous_vikings_cog, meme_cog

import os
from dotenv import load_dotenv


class Bjorn(commands.Bot):

    def __init__(self):
        intents = discord.Intents.all()
        commands.Bot.__init__(self, command_prefix=commands.when_mentioned_or("Bjørn "), intents=intents)

        # Add cogs here
        self.add_cog(basic_cog.Basic())
        self.add_cog(catch_cog.Catch())
        self.add_cog(famous_vikings_cog.FamousVikings())
        self.add_cog(meme_cog.Meme(self))


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bjorn = Bjorn()
bjorn.run(TOKEN)
