from discord.ext import commands
from discord import Embed, Color

from datetime import datetime

from math import floor


class Basic(commands.Cog):

    @commands.command(name='hello')
    async def hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.mention}")

    @commands.command(name='countdown')
    async def countdown(self, ctx, unit='days'):
        viking_date = datetime(2021, 11, 19, 18, 00, 00)
        current_date = datetime.now()

        countdown = viking_date - current_date

        if unit == "days":
            await ctx.send(f"There are {countdown.days} more day(s) until Viking Rally 2021")
        elif unit == "weeks":
            await ctx.send(f"There are {countdown.days / 7} more week(s) until Viking Rally 2021")
        elif unit == "hours":
            await ctx.send(f"There are {floor(countdown.total_seconds() / 3600)} more hour(s) until Viking Rally 2021")
        elif unit == "minutes":
            await ctx.send(f"There are {floor(countdown.total_seconds() / 60)} more minutes(s) until Viking Rally 2021")
        elif unit == "seconds":
            await ctx.send(f"There are {floor(countdown.total_seconds())} more seconds(s) until Viking Rally 2021")

    @commands.command(name='info', aliases=['information', 'rally'])
    async def info(self, ctx):
        embed = Embed(title="Viking Rally 2021", color=Color.purple(), url="https://viking-rally.ssago.org")
        embed.set_image(url="https://scontent-lht6-1.xx.fbcdn.net/v/t1.0-9/126196926_189553799446667_7507836042485066230_n.png?_nc_cat=103&ccb=2&_nc_sid=dd9801&_nc_ohc=q6MUS9CvxMgAX_eyxUa&_nc_ht=scontent-lht6-1.xx&oh=495700278c45c27f8e3347dd9a00655b&oe=5FDC1403") # This is the facebook banner, hence the ungodly url size
        embed.add_field(name="When is it?", value="19th - 21st November 2021", inline=False)
        embed.add_field(name="Where is it?", value="Moor House Adventure Centre, Durham", inline=False)
        embed.add_field(name="Who's running it?", value="NUSSAGG and DUSAGG", inline=False)
        embed.add_field(name="What makes it so special?", value="It's the first SSAGO Rally in the North East for 21 Years!", inline=False)
        embed.set_footer(text="For more information about the Rally, click on 'Viking Rally 2021'", icon_url="https://scontent-lht6-1.xx.fbcdn.net/v/t1.0-9/p960x960/126024485_189553636113350_3374549951797900365_o.png?_nc_cat=106&ccb=2&_nc_sid=85a577&_nc_ohc=AHTAX0o4YIAAX-xICmR&_nc_ht=scontent-lht6-1.xx&oh=708c1ec3789fb4ee98886e9d6cc0a998&oe=5FDC9301")

        await ctx.send(embed=embed)