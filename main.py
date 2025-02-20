import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from command.misc import ping, initial
from command.moderation import warn, mod_event, roles
from command.admin_panel import global_

# Set up logging
logging.basicConfig(level=logging.INFO)

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
roles.roles(bot)
initial.initial(bot)
global_.global_(bot)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the required permissions to run this command.")
    else:
        logging.error(f"An error occurred: {error}")
        await ctx.send("An unexpected error occurred. Please try again later.")

# Run the bot
try:
    bot.run(TOKEN)
except Exception as e:
    logging.error(f"Failed to run the bot: {e}")

