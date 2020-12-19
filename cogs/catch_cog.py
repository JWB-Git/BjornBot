from discord.ext import commands
from discord import Status
import json
import random
import time


class Catch(commands.Cog):

    @commands.command(name='catch', brief="Play catch", help="Play catch with me")
    async def catch(self, ctx):
        choice = random.choices([0, 1, 2], weights=[0.25, 0.25, 0.5], k=1)[0]
        if choice == 0:
            await ctx.send("Uh-oh! I accidentally managed to slice the ball in half with my axe")
        elif choice == 1:
            await ctx.send("Oh no! I went to headbutt the ball but managed to spear it with my helmet's horns instead")
        else:
            with open('data/catch.json', 'r') as catch_file:
                catchers = json.load(catch_file)
            catcher = catchers[str(random.choice(range(len(catchers))))]
            timeout = time.time() + 10
            while time.time() < timeout:
                if int(catcher["id"]) in [member.id for member in ctx.guild.members if member.status == Status.online]:
                    break
                catcher = catchers[str(random.choice(range(len(catchers))))]
            await ctx.send(f"{ctx.author.mention}, I don't have a spare hand to catch with, but I was able to bounce it"
                           f" off my shield over to <@{catcher['bot_id']}> ...")
            if catcher.get("action") is not None:  # checks if bot requires an additional action to be able to catch
                await ctx.send(f"{catcher['action']}")
