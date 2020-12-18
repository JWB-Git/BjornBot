from discord.ext import commands
import discord
import json
import random


class FamousVikings(commands.Cog):

    @commands.command(name="famous", aliases=["famousviking, viking"], breif="Find out about a famous Viking",
                      help="I'll post about a famous Viking, including a short bio and image")
    async def famous(self, ctx):
        try:
            with open('data/famous_vikings.json', 'r', encoding="utf-8") as file:
                vikings = json.load(file)
            viking = vikings[str(random.choice(range(len(vikings))))]
            embed = discord.Embed(title=viking["name"], description="A famous Viking",
                                  colour=discord.Colour.from_rgb(44, 4, 67), url=viking['wiki'])
            if viking["image"] != "":
                embed.set_thumbnail(url=viking["image"])
            embed.add_field(name="About", value=viking["info"], inline=False)
            await ctx.send(embed=embed)
        except FileNotFoundError:
            await ctx.send("Ek gereigir seem til veit einnhverr famous vikings á minuterinn.\n"
                           "Or, in English:\n>>>I don't seem to know any famous Vikings at the minute.")
