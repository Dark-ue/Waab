import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

#import modules
import discord
from discord.ext import commands
from dotenv import load_dotenv
from command import ping
from command.moderation import warn 

#load the token from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

#initialize the bot
intents = discord.Intents.all()
intents.message_content = True #NOQA
bot = commands.Bot(command_prefix='$', intents=intents)

#load the commands
ping.ping(bot)
warn.warn(bot)


#run the bot
bot.run(TOKEN)