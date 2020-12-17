from discord.ext import commands
from discord import Embed, Color

from datetime import datetime

import math

class Birthday(commands.Cog):

    def __init__(self, database):
        self.database = database

    @commands.command(name='birthday')
    async def birthday(self, ctx, case):
        if case == 'help':
            await self.help(ctx)
        elif case == 'read':
            await self.read(ctx)

    async def help(self, ctx):
        pass

    async def read(self, ctx):
        birthdays = self.database.child('birthdays').get()

        for birthday in birthdays.each():
            embed = generate_embed(birthday)
            await ctx.send(embed=embed)


# Useful function for generating birthday embeds
def generate_embed(birthday):
    dateVal = birthday.val()['birthday']

    dateObj = datetime.strptime(dateVal, '%d/%m/%Y')
    today = datetime.now()
    age = today.year - dateObj.year
    if today.month < dateObj.month or (today.month == dateObj.month and today.day < dateObj.day):
        age -= 1

    description = birthday.val()['description']

    embed = Embed(title=birthday.key(), color=Color.purple())
    embed.add_field(name="Birth date", value=dateVal, inline=True)
    embed.add_field(name="Current Age", value=age, inline=True)
    embed.add_field(name="Who", value=description, inline=False)
    embed.set_footer(text="Viking Rally 2021 - 19th to 21st November 2021 @ Moorhouse Adventure Centre, Durham",
                     icon_url="https://scontent-lht6-1.xx.fbcdn.net/v/t1.0-9/p960x960/126024485_189553636113350_3374549951797900365_o.png?_nc_cat=106&ccb=2&_nc_sid=85a577&_nc_ohc=AHTAX0o4YIAAX-xICmR&_nc_ht=scontent-lht6-1.xx&oh=708c1ec3789fb4ee98886e9d6cc0a998&oe=5FDC9301")

    return embed







