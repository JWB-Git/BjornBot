# Cog currently disabled in bot - Redesign needed if to function fully

from discord.ext import commands
from discord import Embed, Color, utils

from datetime import datetime

import math

class Birthday(commands.Cog):

    def __init__(self, database):
        self.database = database

    @commands.command(name='birthday', aliases=['birthdays'])
    async def birthday(self, ctx, case, *info):
        if case == 'help':
            await self.help(ctx)
        elif case == 'read':
            await self.read(ctx)
        elif case == 'add':
            await self.add(ctx, info)

    async def help(self, ctx):
        pass

    async def read(self, ctx):
        birthdays = self.database.child('birthdays').get()

        for birthday in birthdays.each():
            embed = generate_embed(birthday)
            await ctx.send(embed=embed)

    async def add(self, ctx, info):
        role = utils.get(ctx.guild.roles, name="Viking Rally")

        if role in ctx.author.roles:  # If user is part of the viking rally team
            if len(info) == 3:
                name = str(info[0]).replace('-', ' ')
                birthdate = info[1]
                description = str(info[2]).replace('-', ' ')

                self.add_birthday(name, birthdate, description)

                await ctx.send(f'{name}\'s Birthday added successfully')
            else:
                await ctx.send(f'Å nei! I Expected 3 arguments (Name, Birthdate & Description) and got {len(info)}. For the name and description, use - inbetween letters rather than spaces and the birthdate must be in dd/mm/yyyy format! ')

        else:
            await ctx.send('Å nei! Your not a member of the Viking Rally team so you can\'t use this command. Sorry!')

    # Function to add birthday to database
    def add_birthday(self, name, birthdate, description):
        data = {
            'birthday': birthdate,
            'description': description
        }

        self.database.child('birthdays').child(name).set(data)


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







