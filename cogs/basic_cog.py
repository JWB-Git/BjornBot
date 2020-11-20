from discord.ext import commands


class Basic(commands.Cog):

    @commands.command(name='hello')
    async def hello(self, ctx):
        await ctx.send("Hello World!")

