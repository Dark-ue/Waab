import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

#import modules
import discord
from discord.ext import commands
from dotenv import load_dotenv
from command import ping
from command.moderation import warn, mod_event

#load the token from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    raise ValueError("No token found. Please set the DISCORD_TOKEN environment variable.")

#initialize the bot
intents = discord.Intents.all()
intents.message_content = True #NOQA
bot = commands.Bot(command_prefix='$', intents=intents)

#load the commands
ping.ping(bot)
warn.warn(bot)
mod_event.mod_event(bot)

#run the bot
bot.run(TOKEN)