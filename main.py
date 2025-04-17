import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from command.misc import misc
from command.moderation import mod_change
from command.moderation import mod_event, roles
from command.moderation import warn
from command.admin_panel import __global__


# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the token from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    raise ValueError("Create a .env file dumbass")

# Initialize the bot
intents = discord.Intents.all()
intents.message_content = True #NOQA (Do not touch, i will return an error otherwise)
bot = commands.Bot(command_prefix='$', intents=intents)

# Load the commands
warn.warn(bot)

class WarnCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def warn(self, ctx, *, member: str):
        await ctx.send(f"{member} has been warned.")

async def load_cogs():
     cog = [
            "command.moderation.mod_event",
            "command.moderation.mod_change",
            "command.moderation.warn",
            "command.moderation.roles",
            "command.misc.misc",
            "command.admin_panel.__global__"
     ]

     for i in cog:
          await bot.load_extension(i)
@bot.event
async def on_ready():
     await load_cogs()

# this shit handles errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
                embed = discord.Embed(
                     title = "Error",
                     description = f"An unexpected error occured: {error}",
                     color = discord.Color.red()
                       )
                bot_message = await ctx.send(embed=embed)
    
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
                title="Permission Error",
                description="You are missing Manage Messages permission(s) to run this command.",
                color=discord.Color.red()
            )
        bot_message = await ctx.send(embed=embed)


        
    else:
         embed = discord.Embed(
              title="Error",
                description=f"An unexpected error occured: {error}",
                color=discord.Color.red()
         )
         await ctx.message.delete(delay=2)
         await bot_message.delete(delay=2)
        
# Run the bot
try:
    bot.run(TOKEN)
except Exception as e:
    logging.error(f"Failed to run the bot: {e}")
