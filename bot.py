from discord.ext import commands

from cogs import basic_cog

import os
from dotenv import load_dotenv


class Bjorn(commands.Bot):

    def __init__(self):
        commands.Bot.__init__(self, command_prefix=commands.when_mentioned_or("Bjorn "))

        # Add cogs here
        self.add_cog(basic_cog.Basic())


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bjorn = Bjorn()
bjorn.run(TOKEN)