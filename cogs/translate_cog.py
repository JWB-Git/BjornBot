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

        embed.set_footer(text="Old Norse Dictionary provided by https://github.com/stscoundrel/ordbok-json", icon_url="https://scontent-lht6-1.xx.fbcdn.net/v/t1.0-9/p960x960/126024485_189553636113350_3374549951797900365_o.png?_nc_cat=106&ccb=2&_nc_sid=85a577&_nc_ohc=AHTAX0o4YIAAX-xICmR&_nc_ht=scontent-lht6-1.xx&oh=708c1ec3789fb4ee98886e9d6cc0a998&oe=5FDC9301")

        await ctx.send(embed=embed)