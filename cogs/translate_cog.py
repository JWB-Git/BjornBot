from discord.ext import commands
from discord import Embed, Color

import json
import random


class Translate(commands.Cog):

    @commands.command(name="norse", brief="View a random Old Norse word", help="View a random Old Norse word")
    async def norse(self, ctx):
        with open('data/oldNorseToEnglish.json', encoding='utf-8') as norse_file:
            norse_dict = json.load(norse_file)

        index = random.randint(0, len(norse_dict))
        chosen_word = norse_dict[index]

        embed = Embed(title=chosen_word['word'], color=Color.purple())

        embed.add_field(name="Meaning", value=chosen_word['definition'], inline=False)
        embed.add_field(name="Type", value=chosen_word['type'] if chosen_word['type'] != "" else "N/A", inline=True)
        embed.add_field(name="Gender", value=chosen_word['gender'] if chosen_word['gender'] != "" else "None", inline=True)
        embed.add_field(name="Branch", value=chosen_word['branch'], inline=False)

        embed.set_footer(text="Old Norse Dictionary provided by https://github.com/stscoundrel/ordbok-json",
                         icon_url="https://viking-rally.ssago.org/img/events/236/media/Viking%20Rally%20Logo.png")

        await ctx.send(embed=embed)