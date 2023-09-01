import discord
from discord.ext import commands
import pymongo
from mongodb import premium_db
import asyncio


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents, command_prefix='>')

    async def on_ready(self):
        print(f"Logged in as {self.user}")

bot = Bot()

def command_is_premium():
    async def oki(ctx):
        user_id = str(ctx.author.id)
        user_data = premium_db.find_one({"_id": user_id})
        if user_data:
            return True
        else:
            prem = discord.Embed(title=":cross: | You need Premium To use This Command!!.", color=0x2b2d31)
            await ctx.send(embed=prem)
            return False

    return commands.check(oki)


@bot.command()
@command_is_premium() # use this decorator
async def test(ctx):
    await ctx.send("commands are working.!")
    
    
@bot.group(pass_context=True)
async def premium(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Please use the right subcommands like: premium add/remove")


@premium.command()
async def add(ctx, user: discord.User):
    user_id = str(user.id)
    ispe_hai = premium_db.find_one({"_id": user_id})
    if ispe_hai:
        await ctx.send(f"{user.name} is already a premium user.")
    else:
        user_data = {"_id": user_id}
        premium_db.insert_one(user_data)
        e = discord.Embed(title=f"Successfully added {user.name} to Premium", color=0x2b2d31)
        await ctx.send(embed=e)
        
@premium.command()
async def remove(ctx, user: discord.User):
    user_id = str(user.id)
    is_in_premium = premium_db.find_one({"_id": user_id})
    if is_in_premium:
        premium_db.delete_one({"_id": user_id})
        await ctx.send(f"Removed {user.name} from the Premium List.")
    else:
        await ctx.send(f"{user.name} is not in the Premium List.")
        
        
token = ""
bot.run(token)
