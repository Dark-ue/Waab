import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from command import ping
from command.moderation import warn, mod_event

# Set up logging
logging.basicConfig(level=logging.INFO)

# Prevent Python from writing .pyc files
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# Load the token from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    raise ValueError("No token found. Please set the DISCORD_TOKEN environment variable.")

# Initialize the bot
intents = discord.Intents.all()
intents.message_content = True #NOQA
bot = commands.Bot(command_prefix='$', intents=intents)

# Load the commands
ping.ping(bot)
warn.warn(bot)
mod_event.mod_event(bot)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.MissingPermissions):
        pass
        

# Run the bot
try:
    bot.run(TOKEN)
except Exception as e:
    pass