from discord.ext import commands

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